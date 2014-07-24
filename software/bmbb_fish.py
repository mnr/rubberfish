import RPi.GPIO as GPIO
import sys
import signal
import os
import urllib
from urllib.parse import quote_plus
from urllib.request import urlretrieve


class BmBB:
    """ interface with the controls and motors of the big mouth billy bass """
    MOUTH = 16
    TAIL = 18
    HEAD = 22
    PUSH_BUTTON = 15
    OPTICAL_SENSOR = 11
    
    def __init__(self):
        GPIO.setmode(GPIO.BOARD) #use P1 header pin numbering convention
        GPIO.setup(MOUTH, GPIO.OUT) # fish mouth
        GPIO.setup(TAIL, GPIO.OUT) # fish tail
        GPIO.setup(HEAD, GPIO.OUT) # fish head
        GPIO.setup(PUSH_BUTTON, GPIO.IN)  # fish pushbutton
        GPIO.setup(OPTICAL_SENSOR, GPIO.IN)  # fish optical sensor
        # signal.signal(signal.SIGTERM,self.killFish)
        # signal.signal(signal.SIGINT,self.killFish)
        # signal.signal(signal.SIGTSTP,self.killFish)
        os.system('amixer cset numid=3 90%')

    def kill_fish(self):
        GPIO.cleanup() #resets the GPIO state to neutral

    def mouth_open(self):
        GPIO.output(MOUTH,GPIO.HIGH)

    def mouth_close(self):
        GPIO.output(MOUTH,GPIO.LOW)

    def head_up(self):
        GPIO.output(HEAD,GPIO.HIGH)

    def head_back(self):
        GPIO.output(HEAD,GPIO.LOW)

    def tail_up(self):
        GPIO.output(TAIL,GPIO.HIGH)

    def tail_back(self):
        GPIO.output(TAIL,GPIO.LOW)

    def speak(self,say_this):
        safe_say_this_URL = "http://translate.google.com/translate_tts?tl=en&q=" + quote_plus(say_this)
        print (safe_say_this_URL)
        a,b = urlretrieve(safe_say_this_URL,'sayThis.wav')
        os.system('aplay sayThis.wav')
        #os.system('aplay Front_Center.wav')
    
