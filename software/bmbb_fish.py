# rpi.gpio documentation at https://sourceforge.net/p/raspberry-gpio-python/wiki/

import RPi.GPIO as GPIO
import sys
import os
import urllib
from urllib.parse import quote_plus
from urllib.request import urlretrieve


class BmBB:
    """ interface with the controls and motors of the big mouth billy bass """

    # assign names to the GPIO pins. A complete list is in the documentation
    fishMOUTH = 13
    fishTAIL = 11
    fishHEAD = 7
    fishHEAD_reverse = 15
    fishMotorEnable = 18
    PWMstatus = None #declaring PWMstatus here for later assignment

    verbose = False #print debugging?

    def __init__(self):
        GPIO.setmode(GPIO.BOARD) #use P1 header pin numbering convention

        GPIO.cleanup() #make sure the fish is in a known state

        # set up gpio pins for fish
        GPIO.setup(self.fishMOUTH, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.fishTAIL, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.fishHEAD, GPIO.OUT, initial=GPIO.LOW)

        # set up PWM for the enable pin on the motor driver
        self.PWMstatus = GPIO.PWM(self.fishMotorEnable, 50) #frequency 50 hz
        self.PWMstatus.start(0) #duty cycle of zero. Enabled but silent

        # do something to indicate life
        self.mouth()

    def shut_down_fish(self):
        self.PWMstatus.stop() # turn off PWM
        GPIO.cleanup() #resets the GPIO state to neutral

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

    def adjustPWM(self,PWMDutyCycle):
        # where 0.0 <= PWMDutyCycle <= 100.0
        PWMDutyCycle = 100 if PWMDutyCycle > 100 else PWMDutyCycle
        PWMDutyCycle = 0 if PWMDutyCycle < 0 else PWMDutyCycle
        PWMstatus.ChangeDutyCycle(PWMDutyCycle)

    def speak(self,say_this):
        for word in say_this.split():
            min_syllables, max_syllables = count_syllables(word)
            # text-to-speech
            # open and close fishmouth

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
