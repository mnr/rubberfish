#!/bin/sh

# the webcam and audio recording collide when running in the background.
# I've set up this file so we only do one at a time
# started in the background by fish_config.sh

echo "background webcam and sound while loop started"

while 1
do
  fswebcam --background --no-banner --resolution 640x480 -s 20 --log /var/log/fswebcam.log --save /home/pi/rubberfish/visuals/pic_%M%S.jpg
  rec /home/pi/rubberfish/sounds/snd.wav silence 1 .5 2.85% 1 1.0 3.0%  --no-show-progress
done
