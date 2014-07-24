import RPi.GPIO as GPIO
import sys
import signal
import os
import urllib
from urllib.parse import quote_plus
from urllib.request import urlretrieve


class BmBB:
    """ interface with the controls and motors of the big mouth billy bass """
    limbs = {
        'MOUTH':16,
        'TAIL':18,
        'HEAD':22
        }
    
    def __init__(self):
        GPIO.setmode(GPIO.BOARD) #use P1 header pin numbering convention
        GPIO.setup(self.limbs['MOUTH'], GPIO.OUT) # fish mouth
        GPIO.setup(self.limbs['TAIL'], GPIO.OUT) # fish tail
        GPIO.setup(self.limbs['HEAD'], GPIO.OUT) # fish head
        GPIO.setup(15, GPIO.IN)  # fish pushbutton
        GPIO.setup(11, GPIO.IN)  # fish optical sensor
        # signal.signal(signal.SIGTERM,self.killFish)
        # signal.signal(signal.SIGINT,self.killFish)
        # signal.signal(signal.SIGTSTP,self.killFish)
        os.system('amixer cset numid=3 90%')

    def kill_fish(self,sigNum,stackFrame):
        for limb in self.limbs:
            GPIO.output(self.limbs[limb],GPIO.LOW)
        GPIO.cleanup() #resets the GPIO state to neutral
        sys.exit(0)

    def action(self,limb,action,enthusiasm,duration):
        if limb in self.limbs: #check to see if this is properly named
            if action == 'close':
                GPIO.output(self.limbs[limb],GPIO.LOW)
            elif action == 'open':
                # open the limb
                GPIO.output(self.limbs[limb],GPIO.HIGH)
            else:
                # unknown option
                print("unknown action")
        else:
            print("unknown limb")

    def mouth_open(self):
        GPIO.output(self.limbs["MOUTH"],GPIO.HIGH)

    def mouth_close(self):
        GPIO.output(self.limbs["MOUTH"],GPIO.LOW)

    def head_up(self):
        GPIO.output(self.limbs["HEAD"],GPIO.HIGH)

    def head_back(self):
        GPIO.output(self.limbs["HEAD"],GPIO.LOW)

    def tail_up(self):
        GPIO.output(self.limbs["TAIL"],GPIO.HIGH)

    def tail_back(self):
        GPIO.output(self.limbs["TAIL"],GPIO.LOW)

    def speak(self,say_this):
        safe_say_this_URL = "http://translate.google.com/translate_tts?tl=en&q=" + quote_plus(say_this)
        print (safe_say_this_URL)
        a,b = urlretrieve(safe_say_this_URL,'sayThis.wav')
        os.system('aplay sayThis.wav')
        #os.system('aplay Front_Center.wav')
    
