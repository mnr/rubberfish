#!/usr/bin/python

"""
| Board | Wi Pi | BCM | in/out | function |
|---|---|---|---|---|
| 12 | 1 | 18 | in | vent (switch) |
| 16 | 4 | 23 | in | light (switch) |
| 10 | ? | 15 | in | heat (switch) |

camera support from https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=84388
"""

import RPi.GPIO as GPIO
import os
import pygame, sys
from pygame.locals import *
import pygame.camera


class boxControls:
    """ provides access to controls mounted on the pedestal """

    # GPIO pins assigned to the two front-panel switches
    boxVENT = 12
    boxLIGHT = 16
    boxHEAT = 10

    # web cam controls
    width = 640
    height = 480
    windowSurfaceObj = None

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.boxVENT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.boxLIGHT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.boxHEAT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        #initialise pygame
        pygame.init()
        pygame.camera.init()
        #setup window
        self.windowSurfaceObj = pygame.display.set_mode((width,height),1,16)
        #pygame.display.set_caption('Camera')

    def get_boxVENT_STATE(self):
        return GPIO.input(self.boxVENT)

    def get_boxLIGHT_STATE(self):
        return GPIO.input(self.boxLIGHT)

    def get_boxHEAT_STATE(self):
        return GPIO.input(self.boxHEAT)

    def get_visual(self):
        # where_to_save_image = "/home/pi/rubberfish/visuals.saveithere","{:%M%S}".format(datetime.now()),".jpg"
        where_to_save_image = "{}{}{}".format("/home/pi/rubberfish/visuals/pic_","{:%H%M%S}".format(datetime.now()),".jpg")
        cam = pygame.camera.Camera("/dev/video0",(self.width,self.height))
        cam.start()
        #take a picture
        image = cam.get_image()
        cam.stop()
        #save picture
        pygame.image.save(self.windowSurfaceObj,where_to_save_image)
        return where_to_save_image
