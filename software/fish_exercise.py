""" simple program to make sure fish is physically connected """

from bmbb_fish import BmBB
import time

my_fish = BmBB()

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



print("end of exercise")
