# rpi.gpio documentation at https://sourceforge.net/p/raspberry-gpio-python/wiki/
import sys
import RPi.GPIO as GPIO
from time import sleep as sleep
import urllib
from urllib.parse import quote_plus
from urllib.request import urlretrieve
import pyttsx
import wordToSay
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
    SpeechEngine = None
    SpeechCallBack_startword = None # used to disconnect the callback to started-word
    SpeechCallBack_finishutter = None # used to disconnect the callback to finished-utterance
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

        # set up text-to-speech engine
        # pyttsx documentation at http://pyttsx.readthedocs.io/en/latest/
        # python 3 requires this https://github.com/Julian-O/pyttsx
        self.SpeechEngine = pyttsx.init()
        self.SpeechEngine.setProperty('rate', 70)
        self.SpeechCallBack_startword = self.SpeechEngine.connect('started-word', self.onStartWord )
        self.SpeechCallBack_finishutter = self.SpeechEngine.connect('finished-utterance', self.onFinishUtterance )

        # do something to indicate life
        self.mouth()

    def shut_down_fish(self):
        if self.debugMode: print("killing the fish")
        self.PWMstatus.stop() # turn off PWM
        GPIO.cleanup() #resets the GPIO state to neutral
        self.SpeechEngine.disconnect(self.SpeechCallBack_startword) #disconnects a callback
        self.SpeechEngine.disconnect(self.SpeechCallBack_finishutter) #disconnects a callback

    def mouth(self,fishDuration=.5,enthusiasm=75):
        if self.debugMode: print('mouth: duration={durate}, enthusiasm={enth}.'.format(durate=fishDuration, enth=enthusiasm))
        self.adjustPWM(enthusiasm)
        GPIO.output(self.fishMOUTH,GPIO.HIGH)
        sleep(fishDuration)
        GPIO.output(self.fishMOUTH,GPIO.LOW)

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

    def onStartWord(self,nameOfPhrase,locationNumber,lengthOfWord):
        # flaps the mouth for each word * syllables in word
        # called by pyttsx as a call back routine
        thisWordObject = self.SpeechWordObjects[locationNumber]
        """ I'm guessing that the "length" in onStartWord(name : string, location : integer, length : integer) is a measurement of time? Seconds? """
        thisWordObject.setlengthOfWord(lengthOfWord)
        syllableCounter = thisWordObject.wordSyllablesMax
        while (syllableCounter):
            self.mouth(fishDuration=thisWordObject.secondsPerSyllable)
            sleep(thisWordObject.secondsPerSyllable)
            syllableCounter -= 1

    def onFinishUtterance(self,name, completed):
        #name: Name associated with the utterance.
        #completed: True if the utterance was output in its entirety or not.
        self.SpeechWordObjects.clear()

    def speak(self,say_this_phrase):
        # says the phrase, plus animates the fish mouth, head and tail in sync to speech
        for aword in say_this_phrase.split():
            self.SpeechWordObjects.append(new wordToSay(aword)) #create an object for each word
        uniqueNameOfPhrase = uuid.uuid4() #create some unique name to id this phrase
        self.SpeechEngine.say(say_this_phrase, uniqueNameOfPhrase)
        self.SpeechEngine.runAndWait()
