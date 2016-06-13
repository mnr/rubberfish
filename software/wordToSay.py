import uuid

class wordToSay:
    """wordToSay - stash everything needed to know to speak a word"""

    wordsPerMinute = 200 #default words per minute

    wordString = ""
    wordSyllablesMax = 0
    wordSyllablesMin = 0
    wordLength = 0
    secondsPerSyllable = 0
    wordUID = None # will contain a unique string id

    def __init__(self, aWord):
        self.wordString = aWord
        self.wordSyllablesMin,self.wordSyllablesMax = count_syllables(aWord)
        self.wordUID = uuid.uuid4() #generate a unique ID for each word

    def setlengthOfWord(self,seconds):
        """ I'm guessing that the "length" in onStartWord(name : string, location : integer, length : integer) is a measurement of time? maybe Seconds? """
        self.wordLength = seconds
        self.secondsPerSyllable = self.wordSyllablesMax/self.wordLength

    def count_syllables(word):
        # thanks to https://github.com/akkana
        verbose = self.debug #print debugging?

        vowels = ['a', 'e', 'i', 'o', 'u']

        on_vowel = False
        in_diphthong = False
        minsyl = 0
        maxsyl = 0
        lastchar = None

        word = word.lower()
        for c in word:
            is_vowel = c in vowels

            if on_vowel == None:
                on_vowel = is_vowel

            # y is a special case
            if c == 'y':
                is_vowel = not on_vowel

            if is_vowel:
                if verbose: print c, "is a vowel"
                if not on_vowel:
                    # We weren't on a vowel before.
                    # Seeing a new vowel bumps the syllable count.
                    if verbose: print "new syllable"
                    minsyl += 1
                    maxsyl += 1
                elif on_vowel and not in_diphthong and c != lastchar:
                    # We were already in a vowel.
                    # Don't increment anything except the max count,
                    # and only do that once per diphthong.
                    if verbose: print c, "is a diphthong"
                    in_diphthong = True
                    maxsyl += 1
            elif verbose: print "[consonant]"

            on_vowel = is_vowel
            lastchar = c

        # Some special cases:
        if word[-1] == 'e':
            minsyl -= 1
        # if it ended with a consonant followed by y, count that as a syllable.
        if word[-1] == 'y' and not on_vowel:
            maxsyl += 1

        return minsyl, maxsyl
