#!/usr/bin/env python3
"""
watches to see if the fish is talking, then changes the voltage meter
runs in background. Started in fish_config.sh
"""

from bmbb_fish import BmBB
from box_controls import boxControls

my_fish = BmBB()
my_box = boxControls()

while True:
    if my_fish.get_fishIsSpeaking():
        my_box.set_voltage(0)
    else:
        my_box.set_voltage(255)
