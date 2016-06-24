# this version of TextToFishSpeak uses pyttsx
# import pyttsx

class TextToFishSpeak:
    """TextToFishSpeak provides a generic entry to a text to speach routine.
    This may be pyttsx or an online cloud service such as watson"""

    # pyttsx variables
    # SpeechEngine = None
    # SpeechCallBack_startword = None # used to disconnect the callback to started-word
    # SpeechCallBack_finishutter = None # used to disconnect the callback to finished-utterance


    def __init__(self):
        # pyttsx documentation at http://pyttsx.readthedocs.io/en/latest/
        # python 3 requires this https://github.com/Julian-O/pyttsx
        # self.SpeechEngine = pyttsx.init()
        # self.SpeechEngine.setProperty('rate', 70)
        # self.SpeechCallBack_startword = self.SpeechEngine.connect('started-word', self.onStartWord )
        # self.SpeechCallBack_finishutter = self.SpeechEngine.connect('finished-utterance', self.onFinishUtterance )

    def doTextToSpeech (self,stringObjectToSay):
        # stringObjectToSay is an object as created by wordToSay

        # support for pyttsx
        # uniqueNameOfPhrase = uuid.uuid4() #create some unique name to id this phrase
        # self.SpeechEngine.say(say_this_phrase, uniqueNameOfPhrase)
        # self.SpeechEngine.runAndWait()

        pass

    # support function for pyttsx
    def onStartWord(self,nameOfPhrase,locationNumber,lengthOfWord):
        # flaps the mouth for each word * syllables in word
        # called by pyttsx as a call back routine
        thisWordObject = self.SpeechWordObjects[locationNumber]
        thisWordObject.setlengthOfWord(lengthOfWord)
        syllableCounter = thisWordObject.wordSyllablesMax
        while (syllableCounter):
            self.mouth(fishDuration=thisWordObject.secondsPerSyllable)
            sleep(thisWordObject.secondsPerSyllable)
            syllableCounter -= 1

    # support function for pyttsx
    def onFinishUtterance(self,name, completed):
        #name: Name associated with the utterance.
        #completed: True if the utterance was output in its entirety or not.
        self.SpeechWordObjects.clear()
