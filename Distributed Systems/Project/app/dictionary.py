import json
import threading
from random import randint


def loadFile(wordsDict, pangramsDict):
    with open("words_dictionary.json") as json_file:
        words = json.load(json_file)
        for word in words:
            wordsDict[word] = ""
            if len(set(word)) == 7 and 's' not in word:
                pangramsDict[word] = ""


class Dictionary:
    __instance = None

    @staticmethod
    def get_instance():
        if Dictionary.__instance is None:
            with threading.Lock():
                if Dictionary.__instance is None:  # Double locking mechanism
                    Dictionary()
        return Dictionary.__instance

    def __init__(self):

        if Dictionary.__instance is not None:
            raise Exception("This is a singleton!")
        else:
            Dictionary.__instance = self

        self.lock = threading.Lock()
        self.words = {}
        self.pangrams = {}
        loadFile(self.words, self.pangrams)
        self.pangram = str(list(self.pangrams.keys())[randint(0, len(self.pangrams))])

    def getPangram(self):
        return set(self.pangram) # make return set when ready to remove multiples.

    def checkWord(self, string):

        if string in self.words:
            if len(set(string)) == 7 and 's' not in string:
                return "Pangram!"

            return "Valid word."

        else:
            return "Sorry, that is not a valid word."
