from GenericAlgorithm import *

lowerCase = "abcdefghijklmnopqrstuvwxyz"
upperCase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"

chars = lowerCase


def neighbors(pattern, d):
    r = []
    if d <= 0:
        return None

    for i in range(0, len(pattern)+1):
        # insertion
        for letter in chars:
            insertion = pattern[:i] + letter + pattern[i:]
            r.append(insertion)

            recursion = neighbors(insertion, d - 1)
            if recursion:
                r += recursion

    for i in range(0, len(pattern)):
        # deletion
        deletion = pattern[:i] + pattern[i+1:]
        r.append(deletion)

        recursion = neighbors(deletion, d - 1)
        if recursion:
            r += recursion

        # replacement
        for letter in chars:
            replacement = pattern[:i] + letter + pattern[i+1:]
            if letter != pattern[i]:
                r.append(replacement)

                recursion = neighbors(replacement, d - 1)
                if recursion:
                    r += recursion

    return r


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

