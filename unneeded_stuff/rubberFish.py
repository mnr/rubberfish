import RPi.GPIO as GPIO
from time import sleep
from bmbb_fish import BmBB


my_fish = BmBB()



my_fish.tail_up()
sleep(.5)
my_fish.tail_back()
sleep(.5)
my_fish.speak("hello, Dave")
sleep(.5)
my_fish.head_up()
sleep(.5)
my_fish.head_back()
sleep(.5)
my_fish.mouth_open()
sleep(.5)
my_fish.mouth_close()
sleep(.5)
my_fish.kill_fish()
