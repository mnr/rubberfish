#!/usr/bin/python3

# I'm learning how to communicate with watson text-to-speech via websockets
# imports for watson
from watson_developer_cloud.watson_developer_cloud_service import WatsonDeveloperCloudService #copied from authorization_v1.py
#import urllib.parse as urlparse  #copied from authorization_v1.py
from watson_developer_cloud import AuthorizationV1
from watson_developer_cloud import TextToSpeechV1
# imports for websockets
# import asyncio # asyncio is included as part of python 3.4 standard library
#import websockets
import private_WatsonStuff #assumes this file is in the same directory
#import json

authorization = AuthorizationV1(
    username='private_WatsonStuff.WatsonUsername',
    password='private_WatsonStuff.WatsonPassword')

tokenURL = authorization.get_token(url=TextToSpeechV1.default_url)

async def dialogWithWatson():
    websocketURI = "wss://stream.watsonplatform.net/text-to-speech/api/v1/synthesize?"
    websocketURI += "voice=en-US_AllisonVoice"
    websocketURI += "&watson-token=" + tokenURL;
    async with websockets.connect('ws://localhost:8765') as websocket:

        name = input("What's your name? ")
        await websocket.send(name)
        print("> {}".format(name))

        greeting = await websocket.recv()
        print("< {}".format(greeting))

asyncio.get_event_loop().run_until_complete(dialogWithWatson())



"""
# here is how watson recommends you do it
@asyncio.coroutine
def hello():
    websocketURI = "wss://stream.watsonplatform.net/text-to-speech/api/v1/synthesize?"
    websocketURI += "voice=en-US_AllisonVoice"
    websocketURI += "&watson-token=" + token;
    # need to get token from bluemix
    websocket = yield from websockets.connect(websocketURI)

    try:
        name = input("What's your name? ")
        yield from websocket.send(name)
        print("> {}".format(name))

        greeting = yield from websocket.recv()
        print("< {}".format(greeting))

    finally:
        yield from websocket.close()

asyncio.get_event_loop().run_until_complete(hello())

# here is how the websockets github recommends you do it
# https://github.com/aaugustin/websockets/blob/master/example/client.py
#!/usr/bin/env python

import asyncio
import websockets

async def hello():
    async with websockets.connect('ws://localhost:8765') as websocket:

        name = input("What's your name? ")
        await websocket.send(name)
        print("> {}".format(name))

        greeting = await websocket.recv()
        print("< {}".format(greeting))

asyncio.get_event_loop().run_until_complete(hello())
