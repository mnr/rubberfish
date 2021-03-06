#!/usr/bin/env python3
"""
sweeps SQLite for phrases that need to be converted to audio,
handles the conversion,
then inserts the BLOB into the record

runs in background. Started in fish_config.sh
"""

###
# portions related to Bing Text-to-speech are Copyright (c) Microsoft Corporation
#All rights reserved.
#MIT License
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the ""Software""), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
###

import http.client # supports Bing Text-to-speech
import urllib.parse, json # may not need these - supports Bing Text-to-speech
import sqlite3
import time
import datetime
from personality import FishPersonality

myFishPersonality = FishPersonality()

##########################
# Bing TTS variables
apiKey = "fc72371f51a744fe9534aadee99e2b86" # This won't work unless you get the api key from https://www.microsoft.com/cognitive-services/en-us/subscriptions?productId=/products/Bing.Speech.Preview
getAccessParams = ""
getAccessHeaders = {"Ocp-Apim-Subscription-Key": apiKey}

#AccessTokenUri = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken";
AccessTokenHost = "api.cognitive.microsoft.com"
getAccessPath = "/sts/v1.0/issueToken"

openSpeak = "<speak version='1.0' xml:lang='en-us'><voice xml:lang='en-us' "
openSpeak += "xml:gender='Female' "
openSpeak += "name='Microsoft Server Speech Text to Speech Voice "
# note that genderSpeak is defined below and contains the voice name and closing bracket

closeSpeak = "</voice></speak>"

##########################
# Open up an SQLite connection
dbconnect = sqlite3.connect("/home/pi/rubberfish/textToSpeech.db")
dbconnect.row_factory = sqlite3.Row #so to access columns by name
cursor = dbconnect.cursor()


def createTimers(numberOfminutes):
    # returns a time object = now + numberOfminutes
    StartMinuteTimer = datetime.datetime.now()
    EndMinuteTimer = StartMinuteTimer + datetime.timedelta(minutes=numberOfminutes)
    return EndMinuteTimer

countBingRequests = 0
bingOneMinute = createTimers(1) # cap activity to 20 bing calls per second
accessTokenTimeout = datetime.datetime.now() # always get a token first time through loop

while True:
    ##########################
    # this loop:
    #    get string from sqlite3. sort for top priority
    #    convert TTS
    #    save to sqlite3

    cursor.execute("select UID, stringToSay from TTS where audioStream is NULL order by priority, Timestamp  ;")
    rows = cursor.fetchall()

    for row in rows:
        # only make 20 calls to Bing per minute. This is a throttle
        if countBingRequests == 19:
            countBingRequests = 0
            if datetime.datetime.now() < bingOneMinute:
                howLongToWait = bingOneMinute - datetime.datetime.now()
                time.sleep(howLongToWait.seconds)
                bingOneMinute = createTimers(1)

        # bing Authorization Tokens time out in 10 minutes. Do I need a new one?
        if datetime.datetime.now() > accessTokenTimeout: # the Bing TTS authorization token times out after ten minutes
            accessTokenTimeout = createTimers(6) #actually times out in 10 minutes, but being safe
            # Connect to server to get the Access Token
            conn = http.client.HTTPSConnection(AccessTokenHost)
            conn.request("POST", getAccessPath, getAccessParams, getAccessHeaders)
            response = conn.getresponse()
            apiKeyData = response.read()
            conn.close()
            accesstoken = apiKeyData.decode("UTF-8")

        synthWaveHeaders = {"Content-type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
        "Authorization": "Bearer " + accesstoken,
        "X-Search-AppId": "07D3234E49CE426DAA29772419F436CA",
        "X-Search-ClientID": "1ECFAE91408841A480F00935DC390960",
        "User-Agent": "TTSForPython"}

        if myFishPersonality.getGender() == "Male":
            genderSpeak = "(en-US, BenjaminRUS)'>"
        else:
            genderSpeak = "(en-US, ZiraRUS)'>"

        theUID = row[0] # get the UID to access the database
        phraseToSay = row[1] # get the string we are going to convert
        synthWaveBody = openSpeak + genderSpeak +  phraseToSay + closeSpeak

        # Connect to server to synthesize the .wav
        conn = http.client.HTTPSConnection("speech.platform.bing.com")
        conn.request("POST", "/synthesize", synthWaveBody, synthWaveHeaders)
        response = conn.getresponse()

        if response.status == 200:
            # if not 200, then something went wrong. Try it again next time
            synthWaveData = response.read()

            # write the audio file back into the database
            sqlDoThis = 'UPDATE TTS SET audioStream = ?, TTSRequestStatus=? WHERE UID = ?;'
            cursor.execute(sqlDoThis,[sqlite3.Binary(synthWaveData),response.status,theUID]);
        else:
            # save the error code for debugging
            sqlDoThis = 'UPDATE TTS SET TTSRequestStatus=? WHERE UID = ?;'
            cursor.execute(sqlDoThis,[response.status,theUID]);

        conn.close()
        dbconnect.commit()
        countBingRequests += 1
