#!/bin/sh

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

# https://debian-administration.org/article/28/Making_scripts_run_at_boot_time_with_Debian

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
    rec ~/rubberfish/sounds/snd.wav silence 1 .5 2.85% 1 1.0 3.0% vad gain -n −−no−show−progress : newfile : restart & #best so far

    echo "##########"
    echo "Finished with Initial Fish"

    ;;
  stop)
    echo "shutting down the fish"
    python3 ~/rubberfish/software/fishShutdown.py

    ;;
  *)
    echo "Usage: /etc/init.d/fish_config.sh {start|stop}"
    exit 1
    ;;
esac

exit 0
