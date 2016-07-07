#!/usr/bin/python3

# creates a pipe-driven method for telling the fish what to say
# run this as python3 fishControlViaPipe.py &

import bmbb_fish
import os

my_fish = BmBB()


FIFO_PATH = '/tmp/SayThis_Fish'

if os.path.exists(FIFO_PATH):
    os.unlink(FIFO_PATH)

if not os.path.exists(FIFO_PATH):
    os.mkfifo(FIFO_PATH)

pipein = open(FIFO_PATH, 'r')

while True:
    sayThis = pipein.readline()[:-1]
    my_fish.speak(sayThis)
