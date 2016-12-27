#!/usr/bin/python3

# rpi.gpio documentation at https://sourceforge.net/p/raspberry-gpio-python/wiki/
import RPi.GPIO as GPIO
from time import sleep as sleep
import logging


class BmBB:
    """ interface with the controls and motors of the big mouth billy bass """

    # assign names to the GPIO pins. A complete list is in the documentation
    fishMOUTH = 13
    fishTAIL = 11
    fishHEAD = 7
    # fishHEAD_reverse = 15
    fishMotorEnable = 18

    # other variables
    PWMstatus = None #declaring PWMstatus here for later assignment
    SpeechWordObjects = []
    logger = None #declaring logger here for later use

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

        # set up error logging
        self.logger = logging.getLogger('FishControl')
        hdlr = logging.FileHandler('/var/tmp/fish.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.DEBUG)

        # do something to indicate life
        self.mouth()
        # self.speak("Hello. I had a good rest, but it's nice to be back at work.")

    def shut_down_fish(self):
        self.logger.info('killing the fish')
        self.PWMstatus.stop() # turn off PWM
        GPIO.cleanup() #resets the GPIO state to neutral

    def mouth(self,fishDuration=.5,enthusiasm=50):
        # opens the mouth, pauses for fishDuration, then closes the mouth
        self.logger.info('mouth: duration={durate}, enthusiasm={enth}.'.format(durate=fishDuration, enth=enthusiasm))
        self.adjustPWM(enthusiasm)
        GPIO.output(self.fishMOUTH,GPIO.HIGH)
        sleep(fishDuration)
        GPIO.output(self.fishMOUTH,GPIO.LOW)

    def head(self,fishDuration=.4,enthusiasm=75):
        self.logger.info('head: duration={durate}, enthusiasm={enth}.'.format(durate=fishDuration, enth=enthusiasm))
        self.adjustPWM(enthusiasm)
        self.headOut(enthusiasm)
        sleep(fishDuration)
        self.headBack()

    def headOut(self,enthusiasm=75):
        self.logger.info('headOut: enthusiasm={enth}.'.format(enth=enthusiasm))
        self.adjustPWM(enthusiasm)
        GPIO.output(self.fishHEAD,GPIO.HIGH)

    def headBack(self):
        self.logger.info('headBack: No Parameters')
        GPIO.output(self.fishHEAD,GPIO.LOW)

    def tail(self,fishDuration=.4,enthusiasm=75):
        self.logger.info('tail: duration={durate}, enthusiasm={enth}.'.format(durate=fishDuration, enth=enthusiasm))
        self.adjustPWM(enthusiasm)
        GPIO.output(self.fishTAIL,GPIO.HIGH)
        sleep(fishDuration)
        GPIO.output(self.fishTAIL,GPIO.LOW)

    def adjustPWM(self,PWMDutyCycle=50):
        # where 0.0 <= PWMDutyCycle <= 100.0
        PWMDutyCycle = 100 if PWMDutyCycle > 100 else PWMDutyCycle
        PWMDutyCycle = 0 if PWMDutyCycle < 0 else PWMDutyCycle
        self.PWMstatus.ChangeDutyCycle(PWMDutyCycle)

# I pulled "speak" out of this file. I'd like to keep bmbb_fish a pure interface to the hardware and put complex logic somewhere else.
# in this case, speak() is moved to fishControlViaPipe.py
