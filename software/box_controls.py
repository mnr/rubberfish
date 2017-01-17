#!/usr/bin/python
# see https://github.com/mnr/rubberfish/wiki/Raspberry-Pi-GPIO-Pinout for pinouts

import RPi.GPIO as GPIO
from datetime import datetime
import smbus

class boxControls:
    """ provides access to controls mounted on the pedestal """

    """
    # boxControls variables
    # GPIO pins assigned to the two front-panel switches
    switches moved to switch_obj
    boxVENT = 12
    boxLIGHT = 16
    boxHEAT = 10

    fish is speaking moved to bmbb_fish
    fishIsSpeaking = 13
    """

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        """
        switches moved to switch_obj
        GPIO.setup(self.boxVENT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.boxLIGHT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.boxHEAT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.fishIsSpeaking, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        """

    """
    switches moved to switch_obj
    def get_boxVENT_STATE(self):
        return GPIO.input(self.boxVENT)

    def get_boxLIGHT_STATE(self):
        return GPIO.input(self.boxLIGHT)

    def get_boxHEAT_STATE(self):
        return GPIO.input(self.boxHEAT)

    def get_fishIsSpeaking(self):
        return GPIO.input(self.fishIsSpeaking)
    """

    def set_voltage(self,setToThis=0):
        # sets the voltage meter to setToThis
        # This was helpful: http://www.raspberry-projects.com/pi/programming-in-python/i2c-programming-in-python/using-the-i2c-interface-2
        bus = smbus.SMBus(1)
        i2cBusLocation = 0x48
        deviceOffset = 0x41
        # because of the circuit path, there is an inverse relationship between setToThis and the voltage shown
        # for example, setToThis=0 will push the needle to the right
        # Therefore, I'm inverting this value (and range checking)
        setToThis = setToThis if setToThis < 256 else 255
        setToThis = setToThis if setToThis > -1 else 0
        setToThis = 255-setToThis #inverting

        data = [0x41,setToThis]
        bus.write_i2c_block_data(i2cBusLocation, deviceOffset, data)


    def get_visual(self):
        """
        camera support from https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=84388

        import pygame, sys
        from pygame.locals import *
        import pygame.camera

        # this came out of __init__
        #initialise pygame
        pygame.init()
        pygame.camera.init()
        #setup window
        self.windowSurfaceObj = pygame.display.set_mode((self.width,self.height),1,16)
        #pygame.display.set_caption('Camera')

        # web cam controls
        width = 640
        height = 480
        windowSurfaceObj = None
        """
        # where_to_save_image = "/home/pi/rubberfish/visuals.saveithere","{:%M%S}".format(datetime.now()),".jpg"
        # where_to_save_image = "{}{}{}".format("/home/pi/rubberfish/visuals/pic_","{:%H%M%S}".format(datetime.now()),".jpg")
        # return where_to_save_image
        pass
