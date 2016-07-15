"""
| Board | Wi Pi | BCM | in/out | function |
|---|---|---|---|---|
| 12 | 1 | 18 | in | vent (switch) |
| 16 | 4 | 23 | in | light (switch) |
| 10 | ? | 15 | in | heat (switch) |
"""

import RPi.GPIO as GPIO

class boxControls:
    """ provides access to controls mounted on the pedestal """

    # GPIO pins assigned to the two front-panel switches
    boxVENT = 12
    boxLIGHT = 16
    boxHEAT = 10

    def __init__(self):

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.boxVENT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.boxLIGHT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.boxHEAT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def get_boxVENT_STATE(self):
        return GPIO.input(self.boxVENT)

    def get_boxLIGHT_STATE(self):
        return GPIO.input(self.boxLIGHT)

    def get_boxHEAT_STATE(self):
        return GPIO.input(self.boxHEAT)
