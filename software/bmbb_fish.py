import RPi.GPIO as GPIO
import sys
import signal
import os
import threading
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

    verbose = False #print debugging?
    
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

    def pbutton(self,callback_function):
        #threading
        #callback_function()
        pass
    
    def optical_sensor(self,callback_function):
        #threading
        #callback_function()
        pass
    
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
