#!/usr/bin/env python3
"""
watches the three switches on the front panel of the boxControls (LIGHT, VENT, HEAT)
sets up the GPIO interrupt
handles the interrupt

runs in background. Started in fish_config.sh
"""

from switch_obj import boxSwitch
from bmbb_fish import BmBB
import logging


# set up error logging
logger = None #declaring logger here for later use

logger = logging.getLogger('FishControl')
hdlr = logging.FileHandler('/var/tmp/fish.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s %(thread)d %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

my_fish = BmBB()

#######################
# Setting up the Heat Switch
boxHEAT = 10
def HEAT_callback(GPIOpin):
    switchState,switchChanged = switchHeat.get_state()
    if switchChanged:
        switch_status = "on" if switchState else "off"
        my_fish.fishSays("The heat switch was turned " + switch_status)
        logger.info("The heat switch was turned " + switch_status)

switchHeat = boxSwitch(boxHEAT)
switchHeat.set_callback(HEAT_callback)

#######################
# Setting up the Light Switch
boxLIGHT = 16
def LIGHT_callback(GPIOpin):
    switchState,switchChanged = switchLight.get_state()
    if switchChanged:
        switch_status = "on" if switchState else "off"
        my_fish.fishSays("The light switch was turned " + switch_status)
        logger.info("The Light switch was turned " + switch_status)

switchLight = boxSwitch(boxLIGHT)
switchLight.set_callback(LIGHT_callback)

#######################
# Setting up the Vent Switch
boxVENT = 12
def VENT_callback(GPIOpin):
    switchState,switchChanged = switchVent.get_state()
    if switchChanged:
        switch_status = "on" if switchState else "off"
        my_fish.fishSays("The Vent switch was turned " + switch_status)
        logger.info("The Vent switch was turned " + switch_status)

switchVent = boxSwitch(boxVENT)
switchVent.set_callback(VENT_callback)

##### Keep the shell alive
while True:
    pass # loop to keep the python shell open
