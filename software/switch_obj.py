#!/usr/bin/env python3
"""
Class to handle one of the front boxControls (LIGHT, VENT, HEAT)
sets up the GPIO interrupt
handles the interrupt

# boxControls variables
# GPIO pins assigned to the two front-panel switches
boxVENT = 12
boxLIGHT = 16
boxHEAT = 10

usage = GPIO.gpio_function(port)
0 = GPIO.OUT
1 = GPIO.IN
40 = GPIO.SERIAL
41 = GPIO.SPI
42 = GPIO.I2C
43 = GPIO.HARD_PWM
-1 = GPIO.UNKNOWN
"""

import RPi.GPIO as GPIO
import logging



class boxSwitch:
    """ Class to handle one of the front boxControls (LIGHT, VENT, HEAT) """

    mySwitch = None # pin assignment for this switch from RPi GPIO
    logger = None #declaring logger here for later use

    def __init__(self,GPIOpin):
        self.mySwitch = GPIOpin

        # set up error logging
        self.logger = logging.getLogger('FishControl')
        hdlr = logging.FileHandler('/var/tmp/fish.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s %(thread)d %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.DEBUG)

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.mySwitch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.logger.info('init ' + str(GPIOpin))

    def get_state(self):
        self.logger.info('Getting state of pin ' + self.mySwitch)
        return GPIO.input(self.mySwitch)

    def set_callback(self,callbackFunction):
        # Define a threaded callback function to run in another thread when events are detected
        # event_detect returns the GPIO pin that has changed
        #   so the function should look like:
        #   def callback(GPIO_pin_changed):
        #      print("The pin that changed is ",GPIO_pin_changed)
        GPIO.add_event_detect(self.mySwitch, GPIO.BOTH, callback=callbackFunction)
        self.logger.info('set up add_event_detect'+callbackFunction.__name__)
