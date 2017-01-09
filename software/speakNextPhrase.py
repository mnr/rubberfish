#!/usr/bin/env python3
"""
pulls the next phrase from SQLite and plays it.
When that phrase is finished, delete it from SQLite and get the next phrase.
If there are no phrases to speak, then wait until there are.

runs in background. Started in fish_config.sh
"""
import pygame # used to play back the speech file

import sqlite3

# pygame stuff
        # set up pygame
        pygame.mixer.pre_init(4000,-16,2,2048)
        pygame.mixer.init()

asound = pygame.mixer.Sound(synthWaveData)
channel = asound.play()

"""
# print("The synthesized wave length: %d" %(len(synthWaveData)))
# print("playing sound")
asound = pygame.mixer.Sound(synthWaveData)
channel = asound.play()


while channel.get_busy() == True:
    continue
"""



# sqlite stuff
dbconnect = sqlite3.connect("textToSpeech.db")
dbconnect.row_factory = sqlite3.Row
cursor = dbconnect.cursor()
