
class GenericAlgorithm:
    """ Abstract class to be extended to wrap various spelling correction methods """
    # dictionary of words mapped to possible spellings {'misspelled word': {dict of possible correct spellings}}
    def __init__(self,dictionary):
        self.possibleSpellings = {}
        self.name = None
        self.dictionary = dictionary
        self.stats = {'match': 0, 'incorrect': 0, 'no_match': 0, 'perfect_match': 0, 'num_attempted': 0}

    def findCorrections(self, typo):
        """
        Recieves a string that has been misspelled and a dictionary of correct spellings and saves possible
        corrections into self.possibleSpellings
        """
        self.possibleSpellings[typo] = {}
        return
