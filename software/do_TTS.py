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

import http.client, urllib.parse, json # supports Bing Text-to-speech

import sqlite3

# Bing TTS variables
apiKey = "fc72371f51a744fe9534aadee99e2b86" # This won't work unless you get the api key from https://www.microsoft.com/cognitive-services/en-us/subscriptions?productId=/products/Bing.Speech.Preview
getAccessParams = ""
getAccessHeaders = {"Ocp-Apim-Subscription-Key": apiKey}

#AccessTokenUri = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken";
AccessTokenHost = "api.cognitive.microsoft.com"
getAccessPath = "/sts/v1.0/issueToken"

openSpeak = "<speak version='1.0' xml:lang='en-us'><voice xml:lang='en-us' xml:gender='Female' name='Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)'>"
closeSpeak = "</voice></speak>"

synthWaveHeaders = None

        # set up Bing Text-to-speech
        # Connect to server to get the Access Token
        # print ("Connect to server to get the Access Token")
        conn = http.client.HTTPSConnection(self.AccessTokenHost)
        conn.request("POST", self.getAccessPath, self.getAccessParams, self.getAccessHeaders)
        response = conn.getresponse()
        # print(response.status, response.reason)

        apiKeyData = response.read()
        conn.close()

        accesstoken = apiKeyData.decode("UTF-8")
        # print ("Access Token: " + accesstoken)
        self.synthWaveHeaders = {"Content-type": "application/ssml+xml",
        			"X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
        			"Authorization": "Bearer " + accesstoken,
        			"X-Search-AppId": "07D3234E49CE426DAA29772419F436CA",
        			"X-Search-ClientID": "1ECFAE91408841A480F00935DC390960",
        			"User-Agent": "TTSForPython"}

# sqlite stuff
dbconnect = sqlite3.connect("textToSpeech.db")
dbconnect.row_factory = sqlite3.Row
cursor = dbconnect.cursor()

# sample write
# this needs to be a read
cursor.execute('''insert into TTS (priority,stringToSay) values (5, "hello world")''');
dbconnect.commit()

"""
        synthWaveBody = self.openSpeak + phraseToSay + self.closeSpeak

        #Connect to server to synthesize the wave
        # print ("\nConnect to server to synthesize the wave")
        conn = http.client.HTTPSConnection("speech.platform.bing.com")
        conn.request("POST", "/synthesize", synthWaveBody, self.synthWaveHeaders)
        response = conn.getresponse()
        print(response.status, response.reason)

        synthWaveData = response.read()
        conn.close()
        
