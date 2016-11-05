#!/usr/bin/python3

# I'm learning how to communicate with watson text-to-speech via websockets
# imports for watson
# from watson_developer_cloud import TextToSpeechV1
from watson_developer_cloud import TextToSpeechV1
# imports for websockets
import asyncio
import websockets

import private_WatsonStuff #assumes this file is in the same directory


# everything above this line works

"""
{
  "url": "https://stream.watsonplatform.net/text-to-speech/api",
  "password": private_WatsonStuff.WatsonPassword,
  "username": private_WatsonStuff.WatsonUsername
}
"""

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
