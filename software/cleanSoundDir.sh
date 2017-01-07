#!/bin/sh

# cp /home/pi/rubberfish/software/cleanSoundDir.sh /etc/cron.hourly/


find /home/pi/rubberfish/sounds/ -mmin +360 -delete
