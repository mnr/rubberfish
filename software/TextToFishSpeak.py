# this version of TextToFishSpeak uses Watson
# see github.com/watson-developer-cloud/python-sdk
# http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/text-to-speech.html

"""
TextToFishSpeak provides a generic entry to a text to speech routine.
This version implements watson
"""

import json
from os.path import join, dirname, expanduser
from watson_developer_cloud import TextToSpeechV1

def doTextToSpeech (stringObjectToSay="You forgot to tell me what to say"):
    # stringObjectToSay is an object as created by wordToSay
    text_to_speech = TextToSpeechV1(
        username='2cf75972-4837-475a-a0ff-a646dfb94883',
        password='1nIH5xBrttWl')

    audio_file_path = join(expanduser('~'),'speechFromWatson.wav')
    audio_file = open(audio_file_path,'wb')
    audio_file.write(text_to_speech.synthesize(stringObjectToSay,accept='audio/wav',voice="en-US_AllisonVoice"))
    return audio_file_path
