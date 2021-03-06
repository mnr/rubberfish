#!/usr/bin/env python3
"""
pulls the next phrase from SQLite and plays it.
When that phrase is finished, delete it from SQLite and get the next phrase.
If there are no phrases to speak, then wait until there are.

runs in background. Started in fish_config.sh
"""
import pygame # used to play back the speech file
import sqlite3
import logging
import time
import random
from bmbb_fish import BmBB

my_fish = BmBB()

#############################
# set up logging
logger = logging.getLogger('FishControl')
hdlr = logging.FileHandler('/var/tmp/fish.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

# set up pygame
pygame.mixer.pre_init(8000,-16,2,2048)
pygame.mixer.init()

# Open up an SQLite connection
try:
    dbconnect = sqlite3.connect("/home/pi/rubberfish/textToSpeech.db")
except sqlite3.Error as er:
    print ('fish line 20 of speakNextPhrase:', er.message)
    logger.info('fish line 20 of speakNextPhrase: {errormsg}'.format(errormsg=er.message))

dbconnect.row_factory = sqlite3.Row #so to access columns by name
cursor = dbconnect.cursor()

##########################
# loop:
#    get audio blob from sqlite3. sort for top priority
#    play the audio
#    delete the record from sqlite3

while True:
    #cursor.execute("select count(*) from TTS")
    #cursorCount = cursor.fetchone()
    #if cursorCount[0] > 0:
    #     cursor.execute("select UID, audioStream from TTS order by priority, Timestamp limit 1");

    try:
        cursor.execute("select UID, audioStream, stringToSay from TTS where audioStream is not NULL order by priority, Timestamp ;");

    except sqlite3.Error as er:
        print ('speakNextPhrase:', er.message)
        logger.info('speakNextPhrase: {errormsg}'.format(errormsg=er.message))

    rows = cursor.fetchall()
    for row in rows:
        theUID = row[0]
        audioBlobToPlay = row[1]
        stringToSay = row[2]

        asound = pygame.mixer.Sound(audioBlobToPlay)
        # determine length/characters
        soundLength =  asound.get_length() #in seconds
        stringLength = len(stringToSay)
        charsPerSecond = stringLength / soundLength

        stopwatch_start = time.time()
        stopwatch_stop = time.time() + soundLength
        channel = asound.play()

        # randomly bring the head out at the beginning of a phrase
        if random.randrange(1,11) <= 3:
            # bring out head roughly 1/3 of the time 
            my_fish.head(fishDuration=2)

        """
        while time.time() < stopwatch_stop:
            phrasePlayedSoFar = time.time() - stopwatch_start
            stringToSayIndex = round(phrasePlayedSoFar * charsPerSecond)
            stringToSayIndex = 0 if stringToSayIndex < 0 else stringToSayIndex
            stringToSayIndex = (stringLength -1) if stringToSayIndex >= stringLength else stringToSayIndex
            achar = stringToSay[stringToSayIndex]

            if achar == '!':
                # do something for !
                my_fish.head()
            elif achar == '.':
                my_fish.tail()
            elif achar == '-':
                my_fish.head()
            else:
                # every other character (alpha numeric)
                pass
        """

        while channel.get_busy() == True:
            # confirm that the audio track has finished playing
            continue

        # sound has played. Now delete the record from the db
        cursor.execute('delete from TTS where UID=?',[theUID])
        dbconnect.commit()
