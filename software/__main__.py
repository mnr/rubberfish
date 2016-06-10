import sys
from time import sleep as sleep
from bmbb_fish import BmBB
from box_controls import boxControls

def main(args=None):
    """The main routine."""

    my_fish = BmBB()
    my_box = boxControls()

    try:
        while 1:
            my_fish.tail()
            sleep(.5)
            #my_fish.speak("hello, Dave")
            #sleep(.5)
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
                    print ("LIGHT has been thrown to the right")
    except KeyboardInterrupt:
        my_fish.shut_down_fish()


if __name__ == "__main__":
    main()
