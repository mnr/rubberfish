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
import time
from personality import FishPersonality

# set up error logging
logger = None #declaring logger here for later use

logger = logging.getLogger('FishControl')
hdlr = logging.FileHandler('/var/tmp/fish.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s %(thread)d %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

my_fish = BmBB()
myFishPersonality = FishPersonality()

#######################
# Setting up the Heat Switch
boxHEAT = 10
def HEAT_callback(GPIOpin):
    switchState,switchChanged = switchHeat.get_state()
    if switchChanged:
        if switchState:
            my_fish.fishSays("A soft summer night sky above. Heat still radiates. From the pavement beneath your car")
        else:
            timestring = time.strftime("%I %p",time.localtime())
            sayThis = 'It\'s around {}. My feet kiss the cold, hard floor. I should have worn socks'.format(timestring)
            my_fish.fishSays(sayThis)

switchHeat = boxSwitch(boxHEAT)
switchHeat.set_callback(HEAT_callback)

#######################
# Setting up the Light Switch
boxLIGHT = 16
def LIGHT_callback(GPIOpin):
    switchState,switchChanged = switchLight.get_state()
    if switchChanged:
        if switchState:
            my_fish.tail()
        else:
            my_fish.head()

switchLight = boxSwitch(boxLIGHT)
switchLight.set_callback(LIGHT_callback)

#######################
# Setting up the Vent Switch
boxVENT = 12
def VENT_callback(GPIOpin):
    switchState,switchChanged = switchVent.get_state()
    if switchChanged:
        if switchState:
            myFishPersonality.setGender("Female")
            my_fish.fishSays("Hello. My name is Zira.")
        else:
            myFishPersonality.setGender("Male")
            my_fish.fishSays("Hello. My name is Ben.")


switchVent = boxSwitch(boxVENT)
switchVent.set_callback(VENT_callback)

##### Keep the shell alive
while True:
    pass # loop to keep the python shell open
