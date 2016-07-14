#!/bin/bash
# https://debian-administration.org/article/28/Making_scripts_run_at_boot_time_with_Debian
# /etc/init.d/blah

############
# Carry out specific functions when asked to by the system
case "$1" in
  start)

    echo "##########"
    echo "set up control processes for the fish"
    python3 ~/rubberfish/software/fishControlViaPipe.py & # tells the fish what to say

    echo "##########"
    echo "set up for visual processing"
    echo "checking for existence of rubberfish/visuals"
    [ ! -d ~/rubberfish/visuals  ] && mkdir ~/rubberfish/visuals

    echo "start the webcam. Save a jpeg every ten seconds labeled as pic20.jpg"ls -al
    fswebcam --loop 10 --background --no-banner --resolution 640x480 --save ~/rubberfish/visuals/pic%S.jpg

    echo "##########"
    echo "set up for audio processing"
    echo "checking for existence of rubberfish/sounds"
    [ ! -d ~/rubberfish/sounds  ] && mkdir ~/rubberfish/sounds

    # relies on the sox package. sudo apt-get install sox
    # http://sox.sourceforge.net/
    # set up the audiodev so sox know where to look
    export AUDIODEV=hw:1,0
    rec ~/rubberfish/sounds/snd.wav silence 1 .5 2.85% 1 1.0 3.0% vad gain -n  : newfile : restart & #best so far

    echo "##########"
    echo "Finished with Initial Fish"

    ;;
  stop)
    echo "shutting down the fish"
    python3 ~/rubberfish/software/fishShutdown.py

    ;;
  *)
    echo "Usage: /etc/init.d/blah {start|stop}"
    exit 1
    ;;
esac

exit 0

# ############
#
#
# echo "Initializing Fish"
# # load git
# # load python spi library (from spidev)
#
# ##############
# # set up control processes for the fish
# ###
# python3 ~/rubberfish/software/fishControlViaPipe.py & # tells the fish what to say
#
# ##############
# # set up for visual processing
# ###
#
# # test for directory. If not available, mkdir ~/rubberfish/visuals
# echo "checking for existence of rubberfish/visuals"
# [ ! -d ~/rubberfish/visuals  ] && mkdir ~/rubberfish/visuals
#
# # https://www.raspberrypi.org/documentation/usage/webcams/
# # test for fswebcam. If not installed, sudo apt-get install fswebcam
#
# echo "start the webcam. Save a jpeg every ten seconds labeled as pic20.jpg"ls -al
# fswebcam --loop 10 --background --no-banner --resolution 640x480 --save ~/rubberfish/visuals/pic%S.jpg
#
# ##############
# # set up for audio processing
# echo "checking for existence of rubberfish/sounds"
# [ ! -d ~/rubberfish/sounds  ] && mkdir ~/rubberfish/sounds
#
# # relies on the sox package. sudo apt-get install sox
# # http://sox.sourceforge.net/
# # set up the audiodev so sox know where to look
# export AUDIODEV=hw:1,0
# # rec
# #    This will make a collection of files starting with “snd001.wav”.
# # silence
# #    After the word “silence” are two sets of three numbers.
# #    These sets determine the “squelch” behavior.
# #    The first set of three “turn on” recording, and the second three “turn off”.
# #    First three: First # is control. Second # is delay. Third # is threshold.
# #    Second three: First # is control. Second # is length of silence to trigger end.
# #    Reference: http://digitalcardboard.com/blog/2009/08/25/the-sox-of-silence/
# # gain -n normalizes to 0db
# # vad trims silence up to the appearance of human voices
# # rec ~/rubberfish/sounds/snd.wav silence 1 1.0 3.0% -1 0.5 3.0%  : newfile : restart
# # rec ~/rubberfish/sounds/snd.wav silence 1 .3 3% 1 1.0 3.0%  : newfile : restart # starts late. Stops on silence
# # rec ~/rubberfish/sounds/snd.wav silence 1 2.0 2.95% 1 1.0 3.0%  : newfile : restart
# # rec ~/rubberfish/sounds/snd.wav silence 1 .5 2.5% 1 1.0 3.0%  : newfile : restart
# # # sample 2 rec ~/rubberfish/sounds/snd.wav silence 1 .5 2.85% 1 1.0 3.0% gain -n  : newfile : restart #works, but sensitive
# # rec ~/rubberfish/sounds/snd.wav silence 1 .5 -31.0d 1 1.0 3.0% gain -n  : newfile : restart
# # #sample 1 rec ~/rubberfish/sounds/snd.wav silence 1 .5 -31.0d 1 1.0 -31.0d gain -n  : newfile : restart
# # rec ~/rubberfish/sounds/snd.wav silence 1 .5 2.85% 1 1.0 3.0% vad
# rec ~/rubberfish/sounds/snd.wav silence 1 .5 2.85% 1 1.0 3.0% vad gain -n  : newfile : restart & #best so far
#
# # arecord didn't do vox
# # echo "record for 10 seconds, save snd20.wav"
# # arecord -d 10 -D plughw:1,0 ~/rubberfish/sounds/snd%S.wav
