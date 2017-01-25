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

    # set up the SQLite database used for text to speech
    python3 /home/pi/rubberfish/software/init_speechDB.py

    # set up converters and handlers
    python3 /home/pi/rubberfish/software/do_TTS.py &
    python3 /home/pi/rubberfish/software/speakNextPhrase.py &
    python3 /home/pi/rubberfish/software/LightVentHeatirq.py &
    python3 /home/pi/rubberfish/software/fish_head_tail.py &

    # set up personality file
    # if file doesn't exist, create it
    file="/home/pi/rubberfish/fish_personality.json"

    if [[ ! -f $file ]]; then
      touch $file
      echo '{"myers_briggs": "ISTP", "gender": "Male"}' > $file
    fi


    # make sure everyone has permissions
    chmod a+rw /home/pi/rubberfish/fish_personality.json

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
