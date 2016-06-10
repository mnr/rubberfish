# rpi.gpio documentation at https://sourceforge.net/p/raspberry-gpio-python/wiki/

class BmBB:
    """ interface with the controls and motors of the big mouth billy bass """
    import RPi.GPIO as GPIO
    from time import sleep
    import sys
    import urllib
    from urllib.parse import quote_plus
    from urllib.request import urlretrieve
    #import pyttsx
    #import wordToSay

    debug = False #debug flag

    # assign names to the GPIO pins. A complete list is in the documentation
    fishMOUTH = 13
    fishTAIL = 11
    fishHEAD = 7
    fishHEAD_reverse = 15
    fishMotorEnable = 18

    # other variables
    PWMstatus = None #declaring PWMstatus here for later assignment
    #SpeechEngine = None
    #EngineDict = None # used to disconnect a callback


    def __init__(self):
        try:
            self.shut_down_fish() #make sure we are in a known state
        except:
            e = sys.exc_info()[0]
            print( "<p>Error: %s</p>" % e )

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
        #self.SpeechEngine = pyttsx.init()
        #self.SpeechEngine.setProperty('rate', 70)
        #self.EngineDict = self.SpeechEngine.connect('started-word', self.flapMouth )

        # do something to indicate life
        self.mouth()

    def shut_down_fish(self):
        self.PWMstatus.stop() # turn off PWM
        GPIO.cleanup() #resets the GPIO state to neutral
        self.SpeechEngine.disconnect(self.EngineDict) #disconnects the speech engine

    def mouth(self,fishDuration=0,enthusiasm=50):
        self.adjustPWM(enthusiasm)
        GPIO.output(self.fishMOUTH,GPIO.HIGH)
        time.sleep(fishDuration)
        GPIO.output(self.fishMOUTH,GPIO.LOW)

    def head(self,duration=0,enthusiasm=50):
        self.adjustPWM(enthusiasm)
        GPIO.output(self.fishHEAD,GPIO.HIGH)
        time.sleep(fishDuration)
        GPIO.output(self.fishHEAD,GPIO.LOW)

    def tail(self,duration=0,enthusiasm=50):
        self.adjustPWM(enthusiasm)
        GPIO.output(self.fishTAIL,GPIO.HIGH)
        time.sleep(fishDuration)
        GPIO.output(self.fishTAIL,GPIO.LOW)

    def adjustPWM(self,PWMDutyCycle=50):
        # where 0.0 <= PWMDutyCycle <= 100.0
        PWMDutyCycle = 100 if PWMDutyCycle > 100 else PWMDutyCycle
        PWMDutyCycle = 0 if PWMDutyCycle < 0 else PWMDutyCycle
        self.PWMstatus.ChangeDutyCycle(PWMDutyCycle)

    def flapMouth(self,nameOfPhrase,locationNumber,lengthOfWord):
        # flaps the mouth for each word * syllables in word
        # called by pyttsx as a call back routine
        self.mouth()

    def speak(self,say_this_phrase):
        # flapMouth() is set up as a word callback in the init
        uniqueNameOfPhrase = "something" #create some unique name to id this phrase
        self.SpeechEngine.say(say_this_phrase, uniqueNameOfPhrase)
        self.SpeechEngine.runAndWait()
