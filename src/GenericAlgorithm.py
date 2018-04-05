
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

