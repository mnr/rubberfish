import sys
from time import sleep as sleep
from bmbb_fish import BmBB
from box_controls import boxControls
import RPi.GPIO as GPIO
from random import randint


def main(args=None):
    """The main routine."""

    my_fish = BmBB()
    my_box = boxControls()

    try:
        while 1:
            randomEnthusiasm = (randint(0,100))
            randomDuration = (randint(0,10))/10
            my_fish.tail(enthusiasm=randomEnthusiasm,fishDuration=randomDuration)
            sleep(1)
            #my_fish.speak("hello, Dave")
            #sleep(.5)
            my_fish.head(enthusiasm=randomEnthusiasm,fishDuration=randomDuration)
            sleep(1)
            my_fish.mouth(enthusiasm=randomEnthusiasm,fishDuration=randomDuration)
            sleep(1)
            #if GPIO.event_detected(my_box.boxVENT):
            print( my_box.get_boxVent_STATE())

            #if GPIO.event_detected(my_box.boxLIGHT):
            print (my_box.get_boxLIGHT_STATE())

        except KeyboardInterrupt:
            my_fish.shut_down_fish()


if __name__ == "__main__":
    main()
