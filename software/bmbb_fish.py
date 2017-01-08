#!/usr/bin/python3

###
# portions related to Bing Text-to-speech are Copyright (c) Microsoft Corporation
#All rights reserved.
#MIT License
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the ""Software""), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
###

# rpi.gpio documentation at https://sourceforge.net/p/raspberry-gpio-python/wiki/
import RPi.GPIO as GPIO
from time import sleep as sleep
import logging
import threading
import http.client, urllib.parse, json # supports Bing Text-to-speech
import pygame # used to play back the speech file


class BmBB:
    """ interface with the controls and motors of the big mouth billy bass """

    # assign names to the GPIO pins.
    # fishMOUTH = 13 # The mouth is now controlled by hardware
    fishTAIL = 11
    fishHEAD = 7
    # fishHEAD_reverse = 15
    fishMotorEnable = 18

    # Bing TTS variables
    apiKey = "fc72371f51a744fe9534aadee99e2b86" # This won't work unless you get the api key from https://www.microsoft.com/cognitive-services/en-us/subscriptions?productId=/products/Bing.Speech.Preview
    getAccessParams = ""
    getAccessHeaders = {"Ocp-Apim-Subscription-Key": apiKey}

    #AccessTokenUri = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken";
    AccessTokenHost = "api.cognitive.microsoft.com"
    getAccessPath = "/sts/v1.0/issueToken"

    openSpeak = "<speak version='1.0' xml:lang='en-us'><voice xml:lang='en-us' xml:gender='Female' name='Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)'>"
    closeSpeak = "</voice></speak>"

    synthWaveHeaders = None


    # other variables
    PWMstatus = None #declaring PWMstatus here for later assignment
    SpeechWordObjects = []
    logger = None #declaring logger here for later use

    def __init__(self):
        GPIO.cleanup()

        GPIO.setmode(GPIO.BOARD) #use P1 header pin numbering convention

        # set up gpio pins for fish
        # GPIO.setup(self.fishMOUTH, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.fishTAIL, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.fishHEAD, GPIO.OUT, initial=GPIO.LOW)

        # set up PWM for the enable pin on the motor driver
        GPIO.setup(self.fishMotorEnable, GPIO.OUT)
        self.PWMstatus = GPIO.PWM(self.fishMotorEnable, 50) #frequency 50 hz
        self.PWMstatus.start(0) #duty cycle of zero. Enabled but silent

        # set up error logging
        self.logger = logging.getLogger('FishControl')
        hdlr = logging.FileHandler('/var/tmp/fish.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.DEBUG)

        # set up Bing Text-to-speech
        # Connect to server to get the Access Token
        print ("Connect to server to get the Access Token")
        conn = http.client.HTTPSConnection(self.AccessTokenHost)
        conn.request("POST", self.getAccessPath, self.getAccessParams, self.getAccessHeaders)
        response = conn.getresponse()
        print(response.status, response.reason)

        apiKeyData = response.read()
        conn.close()

        accesstoken = apiKeyData.decode("UTF-8")
        print ("Access Token: " + accesstoken)
        self.synthWaveHeaders = {"Content-type": "application/ssml+xml",
        			"X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
        			"Authorization": "Bearer " + accesstoken,
        			"X-Search-AppId": "07D3234E49CE426DAA29772419F436CA",
        			"X-Search-ClientID": "1ECFAE91408841A480F00935DC390960",
        			"User-Agent": "TTSForPython"}

        # set up pygame
        pygame.mixer.pre_init(4000,-16,2,2048)
        pygame.mixer.init()

        # do something to indicate life
        self.head()
        # self.speak("Hello. I had a good rest, but it's nice to be back at work.")

    def shut_down_fish(self):
        self.logger.info('killing the fish')
        self.PWMstatus.stop() # turn off PWM
        GPIO.cleanup() #resets the GPIO state to neutral

    def mouth(self,fishDuration=.5,enthusiasm=50):
        pass # mouth is controlled by hardware. This function deprecated

    def head(self,fishDuration=.4,enthusiasm=60):
        self.logger.info('head: duration={durate}, enthusiasm={enth}.'.format(durate=fishDuration, enth=enthusiasm))
        self.headOut(enthusiasm)
        fishDuration = fishDuration if fishDuration < 1 else 1
        t = threading.Timer(fishDuration,self.headBack)
        t.start() # after 'fishDuration' seconds, the head will return

    def headOut(self,enthusiasm=60):
        self.logger.info('headOut: enthusiasm={enth}.'.format(enth=enthusiasm))
        if enthusiasm > 60:
            enthusiasm = 60 # more than 60 will throw the head past it's limit
        self.adjustPWM(enthusiasm)
        GPIO.output(self.fishHEAD,GPIO.HIGH)

    def headBack(self):
        self.logger.info('headBack: No Parameters')
        GPIO.output(self.fishHEAD,GPIO.LOW)

    def tail(self,fishDuration=.4,enthusiasm=75):
        self.logger.info('tail: duration={durate}, enthusiasm={enth}.'.format(durate=fishDuration, enth=enthusiasm))
        self.tailOut(enthusiasm)
        fishDuration = fishDuration if fishDuration < 1 else 1
        t = threading.Timer(fishDuration,self.tailBack)
        t.start() # after 'fishDuration' seconds, the tail will return

    def tailOut(self,enthusiasm=75):
        self.logger.info('tailOut: enthusiasm={enth}.'.format(enth=enthusiasm))
        self.adjustPWM(enthusiasm)
        GPIO.output(self.fishTAIL,GPIO.HIGH)

    def tailBack(self):
        self.logger.info('tailBack: No Parameters')
        GPIO.output(self.fishTAIL,GPIO.LOW)

    def adjustPWM(self,PWMDutyCycle=50):
        # where 0.0 <= PWMDutyCycle <= 100.0
        PWMDutyCycle = 100 if PWMDutyCycle > 100 else PWMDutyCycle
        PWMDutyCycle = 0 if PWMDutyCycle < 0 else PWMDutyCycle
        self.PWMstatus.ChangeDutyCycle(PWMDutyCycle)

    def fishSays(self,phraseToSay="Hello World"):
        synthWaveBody = self.openSpeak + phraseToSay + self.closeSpeak

        #Connect to server to synthesize the wave
        print ("\nConnect to server to synthesize the wave")
        conn = http.client.HTTPSConnection("speech.platform.bing.com")
        conn.request("POST", "/synthesize", synthWaveBody, self.synthWaveHeaders)
        response = conn.getresponse()
        print(response.status, response.reason)

        synthWaveData = response.read()
        conn.close()
        print("The synthesized wave length: %d" %(len(synthWaveData)))
        print("playing sound")
        asound = pygame.mixer.Sound(synthWaveData)
        channel = asound.play()
        """
        while channel.get_busy() == True:
            continue
        """
