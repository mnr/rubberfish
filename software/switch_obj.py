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

"""

import RPi.GPIO as GPIO

class boxSwitch:
    """ Class to handle one of the front boxControls (LIGHT, VENT, HEAT) """

    mySwitch = None # pin assignment for this switch from RPi GPIO

    def __init__(self,GPIOpin):
        self.mySwitch = GPIOpin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.mySwitch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def get_state(self):
        return GPIO.input(self.mySwitch)

    def set_callback(self,callbackFunction):
        # Define a threaded callback function to run in another thread when events are detected
        # event_detect returns the GPIO pin that has changed
        #   so the function should look like:
        #   def callback(GPIO_pin_changed):
        #      print("The pin that changed is ",GPIO_pin_changed)
        GPIO.add_event_detect(self.mySwitch, GPIO.BOTH, callback=callbackFunction)
