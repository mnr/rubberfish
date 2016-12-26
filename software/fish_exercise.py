""" simple program to make sure fish is physically connected """

from ../software/bmbb_fish import BmBB

my_fish = BmBB()

# mouth
print("mouth start")
my_fish.mouth(fishDuration=.5,enthusiasm=50)
print('mouth end')

# head
print('head start')
my_fish.head(fishDuration=.4,enthusiasm=75)
print('head end')

# tail
print('tail start')
my_fish.tail(fishDuration=.4,enthusiasm=75):
print('tail end')
