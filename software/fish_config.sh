#!/bin/sh

# how to
# https://debian-administration.org/article/28/Making_scripts_run_at_boot_time_with_Debian
# copy this file into /etc/init.d

### BEGIN INIT INFO
# Provides:          fish_config
# Required-Start:    $remote_fs $syslog $time
# Required-Stop:     $remote_fs $syslog $time
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Fish Initialization & Shutdown
# Description:       starts rubber fish software and hardware.
### END INIT INFO

# Author: Mark Niemann-Ross <mark@niemannross.com>

DESC="Fish Initialization & Shutdown"
# DAEMON=/usr/sbin/daemonexecutablename

############
# Carry out specific functions when asked to by the system
case "$1" in
  start)

    # Start a pipe to handle text-to-speech, watson and robotics for the fish
    # python3 /home/pi/rubberfish/software/fishControlViaPipe.py & # tells the fish what to say

    # set up the SQLite database used for text to speech
    rm --force /home/pi/rubberfish/textToSpeech.db # delete any old database
    sqlite3 /home/pi/rubberfish/textToSpeech.db "create table TTS (UID integer primary key, Timestamp DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')), priority integer, stringToSay text, audioStream BLOB)"
    sqlite3 /home/pi/rubberfish/textToSpeech.db 'CREATE UNIQUE INDEX UID on TTS (UID)'
    chmod a+rw /home/pi/rubberfish/textToSpeech.db
    # set up converters and handlers
    python3 /home/pi/rubberfish/software/do_TTS.py &
    python3 /home/pi/rubberfish/software/speakNextPhrase.py &

    # set up for visual processing
    # checking for existence of rubberfish/visuals
    [ ! -d /home/pi/rubberfish/visuals  ] && mkdir /home/pi/rubberfish/visuals

    # webcam moved to sensorProcesses.sh
    # echo "start the webcam. Save a jpeg every ten seconds labeled as pic20.jpg"ls -al
    # fswebcam --loop 10 --background --no-banner --resolution 640x480 -s 20 --log /var/log/fswebcam.log --save /home/pi/rubberfish/visuals/pic_%M%S.jpg


    # set up for audio processing
    # checking for existence of rubberfish/sounds
    [ ! -d /home/pi/rubberfish/sounds  ] && mkdir /home/pi/rubberfish/sounds

    # sox rec works without gain controls
    # relies on the sox package. sudo apt-get install sox
    # http://sox.sourceforge.net/
    # set up the audiodev so sox know where to look
    # export AUDIODEV=hw:1,0 #how it's done in bash
    # here's how it's done in sh
    AUDIODEV=hw:1,0
    export AUDIODEV
    # the following produces "rec FAIL gain: usage: [-e|-b|-B|-r] [-n] [-l|-h] [gain-dB]"
    # rec /home/pi/rubberfish/sounds/snd.wav silence 1 .5 2.85% 1 1.0 3.0% vad gain -n --no-show-progress : newfile : restart & #best so far
    # rec /home/pi/rubberfish/sounds/snd.wav silence 1 .5 2.85% 1 1.0 3.0%  --no-show-progress : newfile : restart &
    # rec is moved to sensorProcesses.sh

    # set a cron job to clear the sound directory every hour
    # cron 3 */1 * * * /home/pi/rubberfish/software/cleanSoundDir.sh
    sudo cp /home/pi/rubberfish/software/cleanSoundDir.sh /etc/cron.hourly/

    # starting background webcam and sound"
    # /home/pi/rubberfish/software/sensorProcesses.sh &
    # the pi keeps going off line. While I'm setting up the comparator, I'm going to shut off
    # the sensor processes

    # Finished with Initial Fish"

    ;;
  stop)
    echo "shutting down the fish"
    python3 /home/pi/rubberfish/software/fishShutdown.py

    # perhaps this should also remove a cron job and kill background processes

    ;;
  *)
    echo "Usage: /etc/init.d/fish_config.sh {start|stop}"
    exit 1
    ;;
esac

exit 0
