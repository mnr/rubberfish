#!/usr/bin/env python3
"""
watches the three switches on the front panel of the boxControls (LIGHT, VENT, HEAT)
sets up the GPIO interrupt
handles the interrupt

runs in background. Started in fish_config.sh
"""

from box_controls import boxControls
from bmbb_fish import BmBB
import RPI_GPIO

my_box = boxControls()
my_fish = BmBB()
GPIO.setmode(GPIO.BOARD)

def LIGHT_callback(GPIOpin):
    switch_status = "on" if my_box.get_boxLIGHT_STATE() else "off"
    saySwitch("Light",switch_status)

def HEAT_callback(GPIOpin):
    switch_status = "on" if my_box.get_boxHEAT_STATE() else "off"
    saySwitch("Heat",switch_status)

def VENT_callback(GPIOpin):
    switch_status = "on" if my_box.get_boxVENT_STATE() else "off"
    saySwitch("Vent",switch_status)

# Define a threaded callback function to run in another thread when events are detected
GPIO.setup(self.boxVENT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(self.boxVENT, GPIO.BOTH, callback=the_handler)

GPIO.setup(self.boxLIGHT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(self.boxLIGHT, GPIO.BOTH, callback=the_handler)

GPIO.setup(self.boxHEAT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(self.boxHEAT, GPIO.BOTH, callback=the_handler)


def say_switch(self,switch_name,switch_status):
    my_fish.fishSays("The ",switch_name," switch was turned ",switch_status)
