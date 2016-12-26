rubberfish
==========

**Embedding a Raspberry Pi into a Big Mouth Billy Bass**

Before you read any further, it's important to review [Installing Linux on a Dead Badger: User's Notes](http://www.strangehorizons.com/2004/20040405/badger.shtml) by Lucy A. Snyder. If I am asked, I will name this as the source of my inspiration.

*The Truth ... I was well into my fish conversion before my friend [David D. Levine](http://www.daviddlevine.com/) pointed out this article.*

**Notes on using IBM watson**

* Here is the [watson text to speech documentation](https://www.ibm.com/watson/developercloud/text-to-speech.html).
* Here is [how to use tts](https://www.ibm.com/watson/developercloud/doc/text-to-speech/index.shtml).
* Here is how to use [watson with websockets](https://www.ibm.com/watson/developercloud/doc/text-to-speech/websockets.shtml#using). This is required if you are going to mark the start of phrases in the wav output.
* Don't forget to upgrade watson. `pip install --upgrade watson-developer-cloud` .


**Notes on installing Websockets**

I'm using [Augustin's websockets for python 3](https://github.com/aaugustin/websockets). I had some problems using `pip install websockets` so resorted to downloading the zip file, cd'ing to the directory and using `sudo python3 setup.py install` .  
* Here is Augustin's documentation on [creating a client](https://github.com/aaugustin/websockets/blob/master/example/client.py) for websockets with python.
* Here's the [websockets pypi page](https://pypi.python.org/pypi/websockets/3.2)


Note that this means you'll be using python3. This library doesn't work with python 2. What's more, it requires Python ≥ 3.4. If you're using Python 3.3 you'll need the asyncio module (`pip install asyncio`).

* Here's some [background on websockets](https://www.fullstackpython.com/websockets.html)
