# rpi.gpio documentation at https://sourceforge.net/p/raspberry-gpio-python/wiki/

import RPi.GPIO as GPIO
import urllib
from urllib.parse import quote_plus
from urllib.request import urlretrieve
import pyttsx

debug = False #debug flag

class BmBB:
    """ interface with the controls and motors of the big mouth billy bass """

    # assign names to the GPIO pins. A complete list is in the documentation
    fishMOUTH = 13
    fishTAIL = 11
    fishHEAD = 7
    fishHEAD_reverse = 15
    fishMotorEnable = 18

    # other variables
    PWMstatus = None #declaring PWMstatus here for later assignment
    SpeechEngine = None


    def __init__(self):
        self.shut_down_fish() #make sure we are in a known state

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
        self.SpeechEngine = pyttsx.init()
        self.SpeechEngine.setProperty('rate', 70)
        engine.connect('started-utterance', self.flapMouth )

        # do something to indicate life
        self.mouth()

    def shut_down_fish(self):
        self.PWMstatus.stop() # turn off PWM
        GPIO.cleanup() #resets the GPIO state to neutral

    def mouth(self,fishDuration=0,enthusiasm=50):
        self.adjustPWM(enthusiasm)
        GPIO.output(self.fishMOUTH,GPIO.HIGH)
        sleep(fishDuration)
        GPIO.output(self.fishMOUTH,GPIO.LOW)

    def head(self,duration=0,enthusiasm=50):
        self.adjustPWM(enthusiasm)
        GPIO.output(self.fishHEAD,GPIO.HIGH)
        sleep(fishDuration)
        GPIO.output(self.fishHEAD,GPIO.LOW)

    def tail(self,duration=0,enthusiasm=50):
        self.adjustPWM(enthusiasm)
        GPIO.output(self.fishTAIL,GPIO.HIGH)
        sleep(fishDuration)
        GPIO.output(self.fishTAIL,GPIO.LOW)

    def adjustPWM(self,PWMDutyCycle=50):
        # where 0.0 <= PWMDutyCycle <= 100.0
        PWMDutyCycle = 100 if PWMDutyCycle > 100 else PWMDutyCycle
        PWMDutyCycle = 0 if PWMDutyCycle < 0 else PWMDutyCycle
        self.PWMstatus.ChangeDutyCycle(PWMDutyCycle)

    def flapMouth(self,name):
        # flaps the mouth once per utterance
        # called by pyttsx as a call back routine
        # required because the callback wants to pass the word, which mouth() doesn't need
        self.mouth()

    def speak(self,say_this_phrase):
        for aSingleWord in say_this_phrase.split():
            # flapMouth() is set up as an utterannce callback in the init
            self.SpeechEngine.say(aSingleWord)
            self.SpeechEngine.runAndWait()
