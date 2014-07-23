import RPi.GPIO as GPIO
from time import sleep
from bmbb_fish import BmBB


myFish = BmBB()


while True:
    myFish.tailUp()
    sleep(.5)
    myFish.tailBack()
    sleep(.5)
    myFish.speak("hello, Dave")
    sleep(.5)
    myFish.headUp()
    sleep(.5)
    myFish.headBack()
    sleep(.5)
    myFish.mouthOpen()
    sleep(.5)
    myFish.mouthClose()
    sleep(.5)

