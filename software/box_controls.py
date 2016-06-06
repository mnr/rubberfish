"""
| Board | Wi Pi | BCM | in/out | function |
|---|---|---|---|---|
| 12 | 1 | 18 | in | vent (switch) |
| 16 | 4 | 23 | in | light (switch) |
"""

class boxControls(object):
    """ provides access to controls mounted on the pedestal """

    boxVENT = 12
    boxLIGHT = 16

    def __init__(self):

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.boxVENT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.boxLIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.boxVENT, GPIO.BOTH, bouncetime=200)
        GPIO.add_event_detect(self.boxLIGHT, GPIO.BOTH, bouncetime=200)


    def get_boxVent_STATE(self):
        return GPIO.input(self.boxVENT)

    def get_boxLIGHT_STATE(self):
        return GPIO.input(self.boxLight)
