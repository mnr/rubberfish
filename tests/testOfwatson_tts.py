#!/usr/bin/python

import json
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1
import private_WatsonStuff


text_to_speech = TextToSpeechV1(
    username=private_WatsonStuff.WatsonUsername,
    password=private_WatsonStuff.WatsonPassword,
    x_watson_learning_opt_out=True)  # Optional flag

# do this mkdir ~/Desktop/watsonspeaks
with open('/users/mnr/Desktop/watsonSpeaks/output.wav', 'wb') as audio_file:
    audio_file.write(text_to_speech.synthesize('Hello world!', accept='audio/wav', voice="en-US_AllisonVoice"))


# print(json.dumps(text_to_speech.voices(), indent=2)) # returns a list of voices

# everything above this line works



# curl -X POST -u 2cf75972-4837-475a-a0ff-a646dfb94883:1nIH5xBrttWl --header "Content-Type: application/json" --header "Accept: audio/wav" --data "{\"text\":\"hello mark\"}" --output hello_world.wav "https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize"

# import pygame
# pygame.mixer.init()
# pygame.mixer.music.load("output.wav")
# pygame.music.mixer.play()
# while pygame.mixer.music.get_busy == True"
#     continue

# coding=utf-8



print(json.dumps(text_to_speech.pronunciation('Watson', pronunciation_format='spr'), indent=2))

print(json.dumps(text_to_speech.customizations(), indent=2))

# print(json.dumps(text_to_speech.create_customization('test-customization'), indent=2))

# print(text_to_speech.update_customization('YOUR CUSTOMIZATION ID', name='new name'))

# print(json.dumps(text_to_speech.get_customization('YOUR CUSTOMIZATION ID'), indent=2))

# print(json.dumps(text_to_speech.get_customization_words('YOUR CUSTOMIZATION ID'), indent=2))

# print(json.dumps(text_to_speech.get_customization_word('YOUR CUSTOMIZATION ID', 'resume'), indent=2))

# print(text_to_speech.delete_customization_word('YOUR CUSTOMIZATION ID', 'resume'))

# print(text_to_speech.delete_customization('YOUR CUSTOMIZATION ID'))
