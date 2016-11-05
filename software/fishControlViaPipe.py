#!/usr/bin/python3

# creates a pipe-driven method for telling the fish what to say
# run this as python3 fishControlViaPipe.py &
# this is run in fish_config.sh

from bmbb_fish import BmBB
import os
from wordToSay import wordToSay
import subprocess
import json
from os.path import join, dirname, expanduser
# for watson
from watson_developer_cloud import TextToSpeechV1
# for websockets
import asyncio
import websockets



my_fish = BmBB()

FIFO_PATH = '/tmp/SayThis_Fish'

if os.path.exists(FIFO_PATH):
    os.unlink(FIFO_PATH)

if not os.path.exists(FIFO_PATH):
    os.mkfifo(FIFO_PATH)

pipein = open(FIFO_PATH, 'r')

while True:
    # says the phrase, plus animates the fish mouth, head and tail in sync to speech
    sayThis = pipein.readline()[:-1]
    if sayThis != '': #if we read something from the pipe, do the following. Otherwise, don't waste the cycles
        # build a dictionary of wordToSay objects. One object per word
        wordDictionary = {}

        for aword in sayThis.split():
            wordIndex = 0
            keyword = aword
            while True:
                if keyword in wordDictionary:
                    wordIndex += 1
                    keyword = aword + str(wordIndex)
                else:
                    break
            wordDictionary[keyword] = wordToSay(aword)






        """ I'm here



        # play each word and animate
        for aword in allwords:
            subprocess.Popen(['aplay', wordDictionary[aword]])

            # animate the fish
            # for aword in say_this_phrase.split():
            minsyl, maxsyl = countSyllables.count_syllables(aword)
            if self.debugMode: print (minsyl,maxsyl,aword)
            mouthPause = (len(aword)/(1 if minsyl == 0 else minsyl))*.05
            # headAndTailRandomizer = random.randint(1,10)
            # if (headAndTailRandomizer > 5): self.head()
            # if (headAndTailRandomizer > 7): self.tail()
            for theIndex in range(1 if minsyl==0 else minsyl):
                self.mouth(fishDuration=mouthPause)
    # this version of TextToFishSpeak uses Watson
    # see github.com/watson-developer-cloud/python-sdk
    # http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/text-to-speech.html
    # sudo pip install --upgrade watson-developer-cloud
    # sudo pip3 install --upgrade watson-developer-cloud


    # TextToFishSpeak provides a generic entry to a text to speech routine.
    # This version implements the text-to-speech as implemented by ibm watson


    def doTextToSpeech (stringObjectToSay="You forgot to tell me what to say"):
        # stringObjectToSay is an object as created by wordToSay
        text_to_speech = TextToSpeechV1(
            username='2cf75972-4837-475a-a0ff-a646dfb94883',
            password='1nIH5xBrttWl')

        separator = "/"
        itzawav = stringObjectToSay+'.wav'
        audio_file_path = join(expanduser('~/rubberfish/words'),itzawav)
        audio_file = open(audio_file_path,'wb')
        audio_file.write(text_to_speech.synthesize(stringObjectToSay,accept='audio/wav',voice="en-US_AllisonVoice"))
        return audio_file_path
