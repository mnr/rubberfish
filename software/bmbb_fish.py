# rpi.gpio documentation at https://sourceforge.net/p/raspberry-gpio-python/wiki/
import sys
import subprocess
import RPi.GPIO as GPIO
from time import sleep as sleep
import urllib
from urllib.parse import quote_plus
from urllib.request import urlretrieve
import TextToFishSpeak
import countSyllables
import uuid

class BmBB:
    """ interface with the controls and motors of the big mouth billy bass """

    debugMode = False #debug flag

    # assign names to the GPIO pins. A complete list is in the documentation
    fishMOUTH = 13
    fishTAIL = 11
    fishHEAD = 7
    fishHEAD_reverse = 15
    fishMotorEnable = 18

    # other variables
    PWMstatus = None #declaring PWMstatus here for later assignment
    SpeechWordObjects = []

    def __init__(self):
        GPIO.cleanup()

        GPIO.setmode(GPIO.BOARD) #use P1 header pin numbering convention

        # set up gpio pins for fish
        GPIO.setup(self.fishMOUTH, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.fishTAIL, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.fishHEAD, GPIO.OUT, initial=GPIO.LOW)

        # set up PWM for the enable pin on the motor driver
        GPIO.setup(self.fishMotorEnable, GPIO.OUT)
        self.PWMstatus = GPIO.PWM(self.fishMotorEnable, 50) #frequency 50 hz
        self.PWMstatus.start(0) #duty cycle of zero. Enabled but silent

        # do something to indicate life
        self.mouth()

    def shut_down_fish(self):
        if self.debugMode: print("killing the fish")
        self.PWMstatus.stop() # turn off PWM
        GPIO.cleanup() #resets the GPIO state to neutral

    def mouth(self,fishDuration=.5,enthusiasm=75):
        if self.debugMode: print('mouth: duration={durate}, enthusiasm={enth}.'.format(durate=fishDuration, enth=enthusiasm))
        self.adjustPWM(enthusiasm)
        GPIO.output(self.fishMOUTH,GPIO.HIGH)
        sleep(fishDuration)
        GPIO.output(self.fishMOUTH,GPIO.LOW)
        sleep(fishDuration)

    def head(self,fishDuration=.4,enthusiasm=75):
        if self.debugMode: print('head: duration={durate}, enthusiasm={enth}.'.format(durate=fishDuration, enth=enthusiasm))
        self.adjustPWM(enthusiasm)
        GPIO.output(self.fishHEAD,GPIO.HIGH)
        sleep(fishDuration)
        GPIO.output(self.fishHEAD,GPIO.LOW)

    def tail(self,fishDuration=.4,enthusiasm=75):
        if self.debugMode: print('tail: duration={durate}, enthusiasm={enth}.'.format(durate=fishDuration, enth=enthusiasm))
        self.adjustPWM(enthusiasm)
        GPIO.output(self.fishTAIL,GPIO.HIGH)
        sleep(fishDuration)
        GPIO.output(self.fishTAIL,GPIO.LOW)

    def adjustPWM(self,PWMDutyCycle=50):
        # where 0.0 <= PWMDutyCycle <= 100.0
        PWMDutyCycle = 100 if PWMDutyCycle > 100 else PWMDutyCycle
        PWMDutyCycle = 0 if PWMDutyCycle < 0 else PWMDutyCycle
        self.PWMstatus.ChangeDutyCycle(PWMDutyCycle)

    def speak(self,say_this_phrase):
        # says the phrase, plus animates the fish mouth, head and tail in sync to speech

        # convert text to speech
        audio_file_path = TextToFishSpeak.doTextToSpeech(say_this_phrase)
        subprocess.Popen(['aplay', audio_file_path])

        # animate the fish
        for aword in say_this_phrase.split():
            minsyl, maxsyl = countSyllables.count_syllables(aword)
            print (minsyl,maxsyl,aword)
            for theIndex in range(1 if minsyl==0 else minsyl):
                self.mouth(fishDuration=.1)
