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

boxHEAT = 10
def HEAT_callback(GPIOpin):
    switch_status = "on" if switchHeat.get_state() else "off"
    print("The heat switch was turned ",switch_status)
    my_fish.fishSays("The heat switch was turned " + switch_status)
    logger.info("The heat switch was turned " + switch_status)


switchHeat = boxSwitch(boxHEAT)
switchHeat.set_callback(HEAT_callback)

boxLIGHT = 16

boxVENT = 12

while True:
    pass # loop to keep the python shell open
