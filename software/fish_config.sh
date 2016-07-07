#!/bin/bash

echo "Initializing Fish"
# load git
# load python spi library (from spidev)

##############
# set up control processes for the fish
###
python3 ~/rubberfish/software/fishControlViaPipe.py & # tells the fish what to say

##############
# set up for visual processing
###

# test for directory. If not available, mkdir ~/rubberfish/visuals
echo "checking for existence of rubberfish/visuals"
[ ! -d ~/rubberfish/visuals  ] && mkdir ~/rubberfish/visuals

# https://www.raspberrypi.org/documentation/usage/webcams/
# test for fswebcam. If not installed, sudo apt-get install fswebcam

# start the webcam. Save a jpeg every ten seconds labeled as pic20.jpg
fswebcam --loop 10 --background --no-banner --resolution 640x480 --save ~/rubberfish/visuals/pic%S.jpg

##############
# set up for audio processing
# arecord -D plughw:1,0 test.wav

echo "Finished with Initial Fish"
