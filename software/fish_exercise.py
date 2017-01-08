""" simple program to make sure fish and box controls are physically connected """

from bmbb_fish import BmBB
from box_controls import boxControls
import time

my_fish = BmBB()
my_box = boxControls()

# BmBB init opens the mouth

# Speech
print('speaking')
my_fish.fishSays("Hello World. It's nice to be here")
sayTheTime = "The time is" + time.strftime("%A, %B %d, %H %M",time.localtime())
my_fish.fishSays(sayTheTime)

# head
print('head start')
my_fish.head(fishDuration=.4,enthusiasm=60)
print('head end')
time.sleep(2)

# tail
print('tail start')
my_fish.tail(fishDuration=.4,enthusiasm=75)
print('tail end')
time.sleep(2)


# voltage meter
print('swing voltage needle')
for setVoltage in range(255):
    my_box.set_voltage(setVoltage)
    print(setVoltage)
    time.sleep(.01)
for setVoltage in range(255,-1,-1):
    my_box.set_voltage(setVoltage)
    print(setVoltage)
    time.sleep(.01)

print("end of exercise")
