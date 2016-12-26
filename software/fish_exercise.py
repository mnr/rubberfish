""" simple program to make sure fish is physically connected """

from bmbb_fish import BmBB
import time

my_fish = BmBB()

# BmBB init opens the mouth

# head
print('head start')
my_fish.head(fishDuration=.4,enthusiasm=75)
print('head end')
time.sleep(2)

# tail
print('tail start')
my_fish.tail(fishDuration=.4,enthusiasm=75)
print('tail end')
time.sleep(2)

# mouth
print("mouth start")
my_fish.mouth(fishDuration=1,enthusiasm=25)
my_fish.mouth(fishDuration=1,enthusiasm=50)
my_fish.mouth(fishDuration=1,enthusiasm=100)
print("mouth end")

print("end of exercise")
