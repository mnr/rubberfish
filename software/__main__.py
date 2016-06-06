import sys
import RPi.GPIO as GPIO
from time import sleep
from bmbb_fish import BmBB

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

my_fish = BmBB()
my_box = boxControls()

my_fish.tail()
sleep(.5)
my_fish.speak("hello, Dave")
sleep(.5)
my_fish.head()
sleep(.5)
my_fish.mouth()
sleep(.5)
if GPIO.event_detected(my_box.boxVENT):
    if my_box.get_boxVent_STATE():
        print ("VENT has been thrown to the left")
    else:
        print("VENT has been thrown to the right")

if GPIO.event_detected(my_box.boxLIGHT):
    if my_box.get_boxLIGHT_STATE():
        print("LIGHT has been thrown to the left")
    else:
        print ("Light has been thrown to the right")


my_fish.shut_down_fish()

"""
try:
    while 1:
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()
"""

if __name__ == "__main__":
    main()
