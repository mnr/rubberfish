#!/usr/bin/python3

# rpi.gpio documentation at https://sourceforge.net/p/raspberry-gpio-python/wiki/
import RPi.GPIO as GPIO
from time import sleep as sleep
import logging
import threading
import sqlite3 # used to write to the tts database
from nltk.tokenize import sent_tokenize # used by saythis() to break into sentences
import nltk

class BmBB:
    """ interface with the controls and motors of the big mouth billy bass """

    # assign names to the GPIO pins.
    # fishMOUTH = 13 # The mouth is now controlled by hardware
    fishTAIL = 11
    fishHEAD = 7
    # fishHEAD_reverse = 15
    fishMotorEnable = 18
    fishIsSpeaking = 13

    # variables for SQlite
    dbconnect = None
    cursor = None

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
        GPIO.setup(self.fishIsSpeaking, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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

        # set up SQLite
        self.dbconnect = sqlite3.connect("/home/pi/rubberfish/textToSpeech.db", check_same_thread=False)
        self.cursor = self.dbconnect.cursor()

        # set up nltk
        # it may be ok to assume these files are available
        # try:
        #    nltk.data.find('punkt.zip')
        #except LookupError:
        #    nltk.download('punkt')

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
        enthusiasm = enthusiasm if enthusiasm < 60 else 60 # more than 60 will throw the head past it's limit
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

    def fishSays(self,phraseToSay="Hello World",priorityToSay=5):
        sqlDoThis = 'insert into TTS (priority,stringToSay) values (?, ?)'
        # break the phrase into sentences
        for aline in sent_tokenize(phraseToSay):
            if aline[-1:] == "?":
                # if this sentence is a question
                awords = aline.split(" ")
                saystring = " ".join(awords[:-1])
                saystring += '<prosody pitch="high">'
                saystring += " ".join(awords[-1:])
                saystring += '</prosody>'
            else:
                saystring = aline
            self.cursor.execute(sqlDoThis,[priorityToSay,saystring]);
            self.dbconnect.commit()

    def get_fishIsSpeaking(self):
        return GPIO.input(self.fishIsSpeaking)

    def fishShutUp(self):
        # stops the fish from talking
        pass
