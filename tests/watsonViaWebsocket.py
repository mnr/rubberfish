# I'm learning how to communicate with watson text-to-speech via websockets
# ### Watson
# watson tts: https://www.ibm.com/watson/developercloud/text-to-speech.html
# using tts: https://www.ibm.com/watson/developercloud/doc/text-to-speech/index.shtml
# using websockets: https://www.ibm.com/watson/developercloud/doc/text-to-speech/websockets.shtml#using

# ### Python
# pypi: https://pypi.python.org/pypi/websockets/3.2
# python tutorial: https://www.fullstackpython.com/websockets.html


# imports for watson
from watson_developer_cloud import TextToSpeechV1
# imports for websockets
import asyncio
import websockets

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
