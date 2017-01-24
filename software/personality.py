#!/usr/bin/env python3
"""
Personality of the fish
"""

import json

class FishPersonality:

    gender = "Female" # random initialization. Note that this isn't binary
    myers_briggs = "ISTP" # random initialization
    personalityFile = "fish_personality.json"

    def __init__(self):
        # check for existence of personalityFile
        try:
            with open(self.personalityFile, 'r', encoding='utf-8') as filePath:
                basic_entry = json.load(filePath)
                self.gender = basic_entry['gender']
                self.myers_briggs = basic_entry['myers_briggs']
        except IOError as e:
            self.updatePersonalityFile() #Does not exist OR no read permissions

    def updatePersonalityFile(self):
        basic_entry = {}
        basic_entry['gender'] = self.gender
        basic_entry['myers_briggs'] = self.myers_briggs

        with open(self.personalityFile, mode='w', encoding='utf-8') as filePath:
            json.dump(basic_entry, filePath, indent=2)

    def getGender(self):
        return self.gender

    def setGender(self,newGender):
        self.gender = newGender
        self.updatePersonalityFile()
