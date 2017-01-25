#!/usr/bin/env python3
"""
Personality of the fish
"""

import json
import os

class FishPersonality:

    basic_entry = {}
    personalityFile = "/home/pi/rubberfish/fish_personality.json"

    def writePersonalityFile(self):
        with open(self.personalityFile, mode='w', encoding='utf-8') as filePath:
            json.dump(self.basic_entry, filePath, indent=2)

    def readPersonalityFile(self):
        with open(self.personalityFile, 'r', encoding='utf-8') as filePath:
                self.basic_entry = json.load(filePath)

    def getGender(self):
        self.readPersonalityFile()
        return basic_entry['gender']

    def setGender(self,newGender):
        self.readPersonalityFile()
        self.basic_entry['gender'] = newGender
        self.writePersonalityFile()
