#!/usr/bin/env python3
"""
Class to handle one of the front boxControls (LIGHT, VENT, HEAT)
sets up the GPIO interrupt
handles the interrupt

"""

import RPi.GPIO as GPIO

class boxSwitch:
    """ Class to handle one of the front boxControls (LIGHT, VENT, HEAT) """

    mySwitch = None # pin assignment for this switch from RPi GPIO

    def __init__(self,GPIOpin):
        self.mySwitch = GPIOpin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.mySwitch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def get_STATE(self):
        return GPIO.input(self.mySwitch)

    def setCallback(self,callbackFunction):
        # Define a threaded callback function to run in another thread when events are detected
        GPIO.add_event_detect(self.mySwitch, GPIO.BOTH, callback=callbackFunction)
