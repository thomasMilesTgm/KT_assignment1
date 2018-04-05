import phonetics
from GenericAlgorithm import *

class Metaphone (GenericAlgorithm):

    def __init__(self, dictionary):
        GenericAlgorithm.__init__(self, dictionary)
        self.phoneticDictionary = {}

        for word in self.dictionary:
            phono = phonetics.metaphone(word)

            try:
                self.phoneticDictionary[phono][word] = 1

            except KeyError:
                self.phoneticDictionary[phono] = {}
                self.phoneticDictionary[phono][word] = 1

        self.name = "metaphone"

    def findCorrections(self, typo):
        if GenericAlgorithm.findCorrections(self, typo):
            pass

        else:
            try:
                phono = phonetics.metaphone(typo)
                if self.phoneticDictionary[phono]:

                    for word in self.phoneticDictionary[phono].keys():

                        self.possibleSpellings[typo][word] = 1

            except KeyError:

                pass


