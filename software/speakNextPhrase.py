#!/usr/bin/env python3
"""
pulls the next phrase from SQLite and plays it.
When that phrase is finished, delete it from SQLite and get the next phrase.
If there are no phrases to speak, then wait until there are.

runs in background. Started in fish_config.sh
"""
import pygame # used to play back the speech file
import sqlite3

# set up pygame
pygame.mixer.pre_init(4000,-16,2,2048)
pygame.mixer.init()

# Open up an SQLite connection
dbconnect = sqlite3.connect("/home/pi/rubberfish/textToSpeech.db")
dbconnect.row_factory = sqlite3.Row #so to access columns by name
cursor = dbconnect.cursor()

##########################
# loop:
#    get audio blob from sqlite3. sort for top priority
#    play the audio
#    delete the record from sqlite3

while True:
    cursor.execute("select count(*) from TTS")
    cursorCount = cursor.fetchone()
    if cursorCount[0] > 0:
        cursor.execute("select UID, audioStream from TTS order by priority, Timestamp limit 1");
        theUID,audioBlobToPlay = cursor.fetchone()

        asound = pygame.mixer.Sound(audioBlobToPlay)
        channel = asound.play()
        while channel.get_busy() == True:
            continue
        # sound has played. Now delete the record
        cursor.execute('delete from TTS where UID=?',[theUID])
        dbconnect.commit()
