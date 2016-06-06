# rpi.gpio documentation at https://sourceforge.net/p/raspberry-gpio-python/wiki/

import RPi.GPIO as GPIO
import sys
import os
import signal
import threading
import urllib
from urllib.parse import quote_plus
from urllib.request import urlretrieve


class BmBB:
    """ interface with the controls and motors of the big mouth billy bass """

    fishMOUTH = 13
    fishTAIL = 11
    fishHEAD = 7
    fishHEAD_reverse = 15
    fishMotorEnable = 18

    verbose = False #print debugging?

    def __init__(self):
        GPIO.setmode(GPIO.BOARD) #use P1 header pin numbering convention

        GPIO.setup(self.fishMOUTH, GPIO.OUT, initial=GPIO.LOW) # fish mouth
        GPIO.setup(self.fishTAIL, GPIO.OUT, initial=GPIO.LOW) # fish tail
        GPIO.setup(self.fishHEAD, GPIO.OUT, initial=GPIO.LOW) # fish head

        """
        GPIO.setup(fishMotorEnable,GPIO.OUT) # Eventually set this to PWM, but this is easy for now
        GPIO.output(fishMotorEnable,GPIO.HIGH)
        """
        enable_pwm_pin = GPIO.PWM(self.fishMotorEnable, frequency)

        # do something to indicate life
        self.mouth()

        # signal.signal(signal.SIGTERM,self.killFish)
        # signal.signal(signal.SIGINT,self.killFish)
        # signal.signal(signal.SIGTSTP,self.killFish)

    def shut_down_fish(self):
        GPIO.output(self.fishMOUTH,GPIO.LOW)
        GPIO.output(self.fishTAIL,GPIO.LOW)
        GPIO.output(self.fishHEAD,GPIO.LOW)
        GPIO.output(self.fishMotorEnable,GPIO.LOW)
        # GPIO.cleanup() #resets the GPIO state to neutral

    def mouth(self,fishDuration=0):
        GPIO.output(self.fishMOUTH,GPIO.HIGH)
        sleep(fishDuration)
        GPIO.output(self.fishMOUTH,GPIO.LOW)

    def head(self,duration=0):
        GPIO.output(self.fishHEAD,GPIO.HIGH)
        sleep(fishDuration)
        GPIO.output(self.fishHEAD,GPIO.LOW)

    def tail(self,duration=0):
        GPIO.output(self.fishTAIL,GPIO.HIGH)
        sleep(fishDuration)
        GPIO.output(self.fishTAIL,GPIO.LOW)

    def speak(self,say_this):
        for word in say_this.split():
            min_syllables, max_syllables = count_syllables(word)
            # text-to-speech
            # open and close fishmouth


        """ using google translate
        safe_say_this_URL = "http://translate.google.com/translate_tts?tl=en&q=" + quote_plus(say_this)
        print (safe_say_this_URL)
        a,b = urlretrieve(safe_say_this_URL,'sayThis.wav')
        os.system('aplay sayThis.wav')
        #os.system('aplay Front_Center.wav')
        """

        """ using pyttsx
        #install: http://electronut.in/making-the-raspberry-pi-speak/
        #https://pypi.python.org/pypi/pyttsx
        #http://pyttsx.readthedocs.org/en/latest/changelog.html
        #http://93.93.128.176/forums/viewtopic.php?f=32&t=58136
        #import pyttsx
        engine = pyttsx.init()
        engine.say("Hello World!")
        engine.runAndWait()
        """

    def count_syllables(word):
        # thanks to https://github.com/akkana
        vowels = ['a', 'e', 'i', 'o', 'u']

        on_vowel = False
        in_diphthong = False
        minsyl = 0
        maxsyl = 0
        lastchar = None

        word = word.lower()
        for c in word:
            is_vowel = c in vowels

            if on_vowel == None:
                on_vowel = is_vowel

            # y is a special case
            if c == 'y':
                is_vowel = not on_vowel

            if is_vowel:
                if verbose: print c, "is a vowel"
                if not on_vowel:
                    # We weren't on a vowel before.
                    # Seeing a new vowel bumps the syllable count.
                    if verbose: print "new syllable"
                    minsyl += 1
                    maxsyl += 1
                elif on_vowel and not in_diphthong and c != lastchar:
                    # We were already in a vowel.
                    # Don't increment anything except the max count,
                    # and only do that once per diphthong.
                    if verbose: print c, "is a diphthong"
                    in_diphthong = True
                    maxsyl += 1
            elif verbose: print "[consonant]"

            on_vowel = is_vowel
            lastchar = c

        # Some special cases:
        if word[-1] == 'e':
            minsyl -= 1
        # if it ended with a consonant followed by y, count that as a syllable.
        if word[-1] == 'y' and not on_vowel:
            maxsyl += 1

        return minsyl, maxsyl
