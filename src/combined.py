from GenericAlgorithm import *
from ngram_distance import *
from neighbors import *
from phonetic import *

""" 
    Uses metaphone algorithm to generate a new dictionary in which ngram can find possible matches
"""

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
