import sys
from time import sleep as sleep
from bmbb_fish import BmBB
from box_controls import boxControls
import RPi.GPIO as GPIO
from random import randint


def main(args=None):
    """The main routine."""

    print("def main variables")
    my_fish = BmBB()
    my_box = boxControls()

    GPIO.add_event_detect(my_box.boxVENT, GPIO.BOTH)
    GPIO.add_event_detect(my_box.boxLIGHT, GPIO.BOTH)
    GPIO.add_event_detect(my_box.boxHEAT, GPIO.BOTH)

    try:
        while 1:
            print("try while 1")
            # randomEnthusiasm = (randint(0,100))
            # randomDuration = (randint(0,10))/10
            # my_fish.tail(enthusiasm=randomEnthusiasm,fishDuration=randomDuration)
            sleep(10)
            # localtime = time.asctime( time.localtime(time.time()) )
            # my_fish.speak("hello, Dave, the time is " + localtime)

            # sidewalkEnds = "Where the Sidewalk Ends by Shel Silverstein. There is a place where the sidewalk ends. And before the street begins,. And there the grass grows soft and white, And there the sun burns crimson bright, And there the moon-bird rests from his flight To cool in the peppermint wind. Let us leave this place where the smoke blows black And the dark street winds and bends. Past the pits where the asphalt flowers grow We shall walk with a walk that is measured and slow, And watch where the chalk-white arrows go To the place where the sidewalk ends. Yes we'll walk with a walk that is measured and slow, And we'll go where the chalk-white arrows go, For the children, they mark, and the children, they know The place where the sidewalk ends. "
            # my_fish.speak(sidewalkEnds)

            # sleep(.5)
            # my_fish.head(enthusiasm=randomEnthusiasm,fishDuration=randomDuration)
            # sleep(1)
            # my_fish.mouth(enthusiasm=randomEnthusiasm,fishDuration=randomDuration)
            # sleep(1)
            print('vent:{ventValue}, light:{lightValue}, heat:{heatValue}.'.format(ventValue=my_box.get_boxVENT_STATE(), lightValue=my_box.get_boxLIGHT_STATE(), heatValue=my_box.get_boxHEAT_STATE()))
            # if GPIO.event_detected(my_box.boxVENT):
            #     if my_box.get_boxVENT_STATE():
            #         print ("VENT has been thrown to the left")
            #     else:
            #         print("VENT has been thrown to the right")
            #
            # if GPIO.event_detected(my_box.boxLIGHT):
            #     if my_box.get_boxLIGHT_STATE():
            #         print("LIGHT has been thrown to the left")
            #     else:
            #         print ("LIGHT has been thrown to the right")
            #
            # if GPIO.event_detected(my_box.boxHEAT):
            #     if my_box.get_boxHEAT_STATE():
            #         print("HEAT has been thrown to the left")
            #     else:
            #         print ("HEAT has been thrown to the right")
            # print (my_box.get_visual()) # trigger the webcam


    except KeyboardInterrupt:
        my_fish.shut_down_fish()


if __name__ == "__main__":
    main()
