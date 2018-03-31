from GenericAlgorithm import *

lowerCase = "abcdefghijklmnopqrstuvwxyz"
upperCase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"

chars = lowerCase

def neighbors(pattern, d):
    assert(d <= len(pattern))

    if d == 0:
        return [pattern]

    r2 = neighbors(pattern[1:], d-1)
    r = [c + r3 for r3 in r2 for c in chars if c != pattern[0]]

    if (d < len(pattern)):
        r2 = neighbors(pattern[1:], d)
        r += [pattern[0] + r3 for r3 in r2]

    return r

class NeighborhoodSearch(GenericAlgorithm):

    def __init__(self, dictionary, distance):
        GenericAlgorithm.__init__(self, dictionary)
        self.distance = distance

    def findCorrections(self, typo):
        self.possibleSpellings[typo] = {}

        if typo in self.dictionary.keys():
            # check for an exact match
            self.possibleSpellings[typo][typo] = 1

        else:
            # otherwise do the neighborhood search
            permute = neighbors(typo, self.distance)

            for permutation in permute:
                try:
                    if self.dictionary[permutation]:
                        self.possibleSpellings[typo][permutation] = 1

                except KeyError:
                    pass

