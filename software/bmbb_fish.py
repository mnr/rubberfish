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
        'mouth':16,
        'tail':18,
        'head':22
        }
    
    def __init__(self):
        GPIO.setmode(GPIO.BOARD) #use P1 header pin numbering convention
        GPIO.setup(self.limbs['mouth'], GPIO.OUT) # fish mouth
        GPIO.setup(self.limbs['tail'], GPIO.OUT) # fish tail
        GPIO.setup(self.limbs['head'], GPIO.OUT) # fish head
        GPIO.setup(15, GPIO.IN)  # fish pushbutton
        GPIO.setup(11, GPIO.IN)  # fish optical sensor
        # signal.signal(signal.SIGTERM,self.killFish)
        # signal.signal(signal.SIGINT,self.killFish)
        # signal.signal(signal.SIGTSTP,self.killFish)
        os.system('amixer cset numid=3 90%')

    def killFish(self,sigNum,stackFrame):
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

    def mouthOpen(self):
        GPIO.output(self.limbs["mouth"],GPIO.HIGH)

    def mouthClose(self):
        GPIO.output(self.limbs["mouth"],GPIO.LOW)

    def headUp(self):
        GPIO.output(self.limbs["head"],GPIO.HIGH)

    def headBack(self):
        GPIO.output(self.limbs["head"],GPIO.LOW)

    def tailUp(self):
        GPIO.output(self.limbs["tail"],GPIO.HIGH)

    def tailBack(self):
        GPIO.output(self.limbs["tail"],GPIO.LOW)

    def speak(self,sayThis):
        safeSayThisURL = "http://translate.google.com/translate_tts?tl=en&q=" + quote_plus(sayThis)
        print (safeSayThisURL)
        a,b = urlretrieve(safeSayThisURL,'sayThis.wav')
        os.system('aplay sayThis.wav')
        #os.system('aplay Front_Center.wav')
    
