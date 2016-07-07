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

echo "start the webcam. Save a jpeg every ten seconds labeled as pic20.jpg"ls -al
fswebcam --loop 10 --background --no-banner --resolution 640x480 --save ~/rubberfish/visuals/pic%S.jpg

##############
# set up for audio processing
echo "checking for existence of rubberfish/sounds"
[ ! -d ~/rubberfish/sounds  ] && mkdir ~/rubberfish/sounds

# relies on the sox package. sudo apt-get install sox
# http://sox.sourceforge.net/
# rec
#    This will make a collection of files starting with “snd001.wav”.
#    -r is bit rate
# silence
#    After the word “silence” are two sets of three numbers.
#    These sets determine the “squelch” behavior.
#    The first set of three “turn on” recording, and the second three “turn off”.
#    First three: First # is control. Second # is delay. Third # is threshold.
#    Second three: First # is control. Second # is length of silence to trigger end.
# rec -r 8000 -t plughw:1,0 snd.wav silence 1 1.0 5% 1 3.0 5%  : newfile : restart

# echo "record for 10 seconds, save snd20.wav"
# arecord -d 10 -D plughw:1,0 ~/rubberfish/sounds/snd%S.wav

echo "Finished with Initial Fish"
