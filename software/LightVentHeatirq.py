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
# poems by Brian Garrison - haikooligan@gmail.com
phraseToSay_one = """What kind of clothes would they wear,
the little fishes of the lake?
Would they collect tiny pebbles in their pockets
or carry extra scales for when their own float off?
Would the big ones strap on large, artificial fins
to play shark games along the shore?
Would they wear mittens to ward off winter’s chill,
and ball caps to block the summer sun?
Would they be modest? Would they be vain?
Would they admire the fishery tags and hope
to one day score a piercing of their own?
Would they worry that their tails are looking fat?"""

phraseToSay_two = """Do fish tell
abduction stories, huddled
around in conference rooms
of run-down hotels
or in the calm eddies of
lesser-known riverbanks
recounting the horrific tales
of laying on dry rocks, being
probed in the gills,
and passing out?
And having nothing more
than their hazy dusk
memories,
do they wonder if maybe
five-fingered mammals
don't really exist?"""
#######################
# Setting up the Heat Switch
boxHEAT = 10
def HEAT_callback(GPIOpin):
    switchState,switchChanged = switchHeat.get_state()
    if switchChanged:
        if switchState:
            my_fish.fishSays(phraseToSay_one)
        else:
            #timestring = time.strftime("%I %p",time.localtime())
            #sayThis = 'It\'s around {} in London. My feet kiss the cold, hard floor. I should have worn socks'.format(timestring)
            my_fish.fishSays(phraseToSay_two)

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
