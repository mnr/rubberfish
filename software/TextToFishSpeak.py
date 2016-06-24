# this version of TextToFishSpeak uses Watson
# see github.com/watson-developer-cloud/python-sdk

import json
import wordToSay
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1

class TextToFishSpeak:
    """
    TextToFishSpeak provides a generic entry to a text to speech routine.
    This version implements watson
    http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/text-to-speech.html
    """

    text_to_speech = TextToSpeechV1(
        username='2cf75972-4837-475a-a0ff-a646dfb94883',
        password='1nIH5xBrttWl')

    def __init__(self):
        pass



    def doTextToSpeech (self,stringObjectToSay):
        # stringObjectToSay is an object as created by wordToSay

audio_file_path = join(os.path.expanduser('~'),'output.wav')
audio_file = open(audio_file_path,'wb')
audio_file.write(text_to_speech.synthesize('Hello world!',accept='audio/wav',voice="en-US_AllisonVoice"))

# to play
import pygame
pygame.mixer.init()
pygame.mixer.music.load(audio_file_path)
pygame.mixer.music.play()

        with open(join(os.path.expanduser('~'), 'output.wav'), 'wb') as audio_file:
            audio_file.write(text_to_speech.synthesize('Hello world!'))

        jsonData = {"con1":40, "con2":20, "con3":99, "con4":40, "password":"1234"}
        URLforService = 'http://watson something'
        params = json.dumps(jsonData).encode('utf8')
        req = urllib.request.Request(URLforService, data=params,
                             headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(req)
        #print(response.read().decode('utf8'))
