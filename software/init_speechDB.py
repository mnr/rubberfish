#!/usr/bin/env python3
"""
Sets up the SQlite database used to queue speech requests

Started in fish_config.sh
"""
import sqlite3
import os

pathToDB = "/home/pi/rubberfish/textToSpeech.db"
# pathToDB = "textToSpeech.db"

##########################
# Open up an SQLite connection
# dbconnect = sqlite3.connect(pathToDB)
dbconnect = sqlite3.connect(pathToDB)
dbconnect.row_factory = sqlite3.Row #so to access columns by name
cursor = dbconnect.cursor()

# rm --force pathToDB # delete any old database
cursor.execute("create table TTS (UID integer primary key, Timestamp DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')), priority integer, stringToSay text, audioStream BLOB)")
cursor.execute('CREATE UNIQUE INDEX UID on TTS (UID)')
dbconnect.commit()
dbconnect.close()

os.chmod(pathToDB, 0o666)

# chmod a+rw /home/pi/rubberfish/textToSpeech.db
