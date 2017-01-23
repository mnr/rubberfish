#!/usr/bin/env python3

""" simple program to make sure fish and box controls are physically connected """

from bmbb_fish import BmBB
import sys

my_fish = BmBB()

# Speech
my_fish.fishSays(sys.argv[1])
# print(sys.argv[1])
