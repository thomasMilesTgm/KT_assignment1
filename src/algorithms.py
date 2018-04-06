import ngram
from utils import *
import phonetics


class AlgoFactory:

    def __init__(self, dictionary, params):
        self.dictionary = dictionary
        self.params = params

    def getAlgo(self, key):
        if key == 'nei':
            return NeighborhoodSearch(self.dictionary, self.params['Neighborhood distance'])
        elif key == 'ng':
            return NgramAlgorithm(self.dictionary, self.params['NGram distance'], self.params['NGram threshold'])
        elif key == 'ngm':
            return metaphone_ngram(self.dictionary, self.params['Metaphone nGrams'], self.params['Metaphone nG threshold'])
        elif key == 'nem':
            return metaphone_neighborhood(self.dictionary, self.params['Metaphone neighbors'])
        elif key == 'meta':
            return Metaphone(self.dictionary)
        else:
            return GenericAlgorithm(self.dictionary)


class GenericAlgorithm:
    """ Abstract class to be extended to wrap various spelling correction methods """
    # dictionary of words mapped to possible spellings {'misspelled word': {dict of possible correct spellings}}
    def __init__(self,dictionary):
        self.possibleSpellings = {}
        self.name = None
        self.dictionary = dictionary
        self.stats = {'match': 0, 'incorrect': 0, 'perfect_match': 0, 'num_attempted': 0}
        self.evaluation = {'precision': 0, 'recall': 0, 'accuracy': 0}
        self.name = "Generic Algorithm"

    def findCorrections(self, typo):
        """
        Recieves a string that has been misspelled and a dictionary of correct spellings and saves possible
        corrections into self.possibleSpellings
        """
        self.possibleSpellings[typo] = {}

        # all spellcheck algorithms should immediately return a match if the misspelled word is already
        # in the dictionary. This can be used as a ground truth for number of words not misspelled according
        # to the dictionary
        try:

            if self.dictionary[typo]:
                # check for an exact match
                self.possibleSpellings[typo][typo] = 1
                return True

        except KeyError:
            return False


class NeighborhoodSearch(GenericAlgorithm):

    def __init__(self, dictionary, distance):
        GenericAlgorithm.__init__(self, dictionary)
        self.distance = distance
        self.name = "Neighborhood Distance"


    def findCorrections(self, typo):

        if GenericAlgorithm.findCorrections(self, typo):
            pass

        else:
            # otherwise do the neighborhood search
            permute = neighbors(typo, self.distance)

            for permutation in permute:
                try:
                    if self.dictionary[permutation]:
                        self.possibleSpellings[typo][permutation] = 1

                except KeyError:
                    pass




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


class metaphone_ngram(Metaphone):
    def __init__(self, dictionary, N, match_threshold=1.0):
        Metaphone.__init__(self, dictionary)
        self.n = N
        self.match_threshold = match_threshold
        self.name = 'Metaphone-nGram'

    def findCorrections(self, typo):

        # first use metaphone to find possible spellings of the word
        Metaphone.findCorrections(self, typo)
        phoneticDict = self.possibleSpellings[typo]

        # then use nGram distance on those spellings with typo to refine solution
        nGram = NgramAlgorithm(phoneticDict, self.n, self.match_threshold)
        nGram.findCorrections(typo)

        self.possibleSpellings[typo] = nGram.possibleSpellings[typo]


class metaphone_neighborhood(Metaphone):
    def __init__(self, dictionary, N):
        Metaphone.__init__(self, dictionary)
        self.n = N
        self.name = 'Metaphone-neighborhood'

    def findCorrections(self, typo):

        # first use metaphone to find possible spellings of the word
        Metaphone.findCorrections(self, typo)
        phoneticDict = self.possibleSpellings[typo]

        # then use neighborhood search on those spellings with typo to refine solution
        nei = NeighborhoodSearch(phoneticDict, 1)
        nei.findCorrections(typo)
        self.possibleSpellings[typo] = nei.possibleSpellings[typo]
