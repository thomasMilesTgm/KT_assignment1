import ngram
from GenericAlgorithm import *

class NgramAlgorithm(GenericAlgorithm):

    def __init__(self, dictionary, N, match_threshold = 1.0):
        """ match threshold from 0.0 - 1.0, where higher value indicates closer n gram distance
            to be considered as a possible match
        """
        GenericAlgorithm.__init__(self, dictionary)
        #self.nGram = ngram.NGram([], key=lambda x:x.lower(), N=N)
        self.n = N
        self.nGramDict = {}
        self.threshold = match_threshold
        self.name = "NGram Distance"

        # save words in a dictionary of NGram lists based on length of the word
        for word in dictionary:
            key = str(len(word))

            if key in self.nGramDict.keys():
                self.nGramDict[key].add(word)

            else:
                self.nGramDict[key] = ngram.NGram(key=lambda x: x.lower(), N=self.n)
                self.nGramDict[key].add(word)

        self.match_threshold = match_threshold

    def findCorrections(self, typo):
        if GenericAlgorithm.findCorrections(self, typo):
            pass

        else:
            for key in range(len(typo)-self.n, len(typo) + self.n):

                try:
                    matches = self.nGramDict[str(key)].search(typo, threshold=self.match_threshold)
                    for match in matches:
                        self.possibleSpellings[typo][match[0]] = 1

                except KeyError:
                    pass


