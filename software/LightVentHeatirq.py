#!/usr/bin/env python3
"""
watches the three switches on the front panel of the boxControls (LIGHT, VENT, HEAT)
sets up the GPIO interrupt
handles the interrupt

runs in background. Started in fish_config.sh
"""

from box_controls import boxControls
from bmbb_fish import BmBB

my_box = boxControls()
my_fish = BmBB()

# Define a threaded callback function to run in another thread when events are detected
def LIGHT_callback(GPIOpin):
    switch_status = "on" if my_box.get_boxLIGHT_STATE() else "off"
    saySwitch("Light",switch_status)

my_box.set_boxLIGHT_IRQ(LIGHT_callback)

def HEAT_callback(GPIOpin):
    switch_status = "on" if my_box.get_boxHEAT_STATE() else "off"
    saySwitch("Heat",switch_status)

my_box.set_boxHEAT_IRQ(HEAT_callback)

def VENT_callback(GPIOpin):
    switch_status = "on" if my_box.get_boxVENT_STATE() else "off"
    saySwitch("Vent",switch_status)

my_box.set_boxVENT_IRQ(VENT_callback)


def say_switch(self,switch_name,switch_status):
    my_fish.fishSays("The ",switch_name," switch was turned ",switch_status)
