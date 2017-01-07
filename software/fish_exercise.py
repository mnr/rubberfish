""" simple program to make sure fish and box controls are physically connected """

from bmbb_fish import BmBB
from box_controls import boxControls
import time

my_fish = BmBB()
my_box = boxControls()

# BmBB init opens the mouth

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
    time.sleep(.1)
for setVoltage in range(255,-1,-1):
    my_box.set_voltage(setVoltage)
    print(setVoltage)
    time.sleep(.1)

print("end of exercise")
