from GenericAlgorithm import *
from neighbors import NeighborhoodSearch

N_DIST = 1 # neighborhood distance
N_GRAM = 2 # nGrams

if __name__=="__main__":

    dictFilepath = "../data_19mar/dictionary.txt"
    misspell = open("../data_19mar/misspell.txt",'r').readlines()
    output = open("../out/statistics.txt", "w")
    correct = open('../data_19mar/correct.txt', 'r').readlines()


    dictionary = {}
    correctSpelling = {}

    # convert the dictionary into a dict, strip \n
    for word in open(dictFilepath, 'r'):
        word = word.strip('\n')
        dictionary[word] = 1

    # define the ground truth
    for i in range(0, len(misspell)):
        correctSpelling[ misspell[i].strip('\n') ] = correct[i].strip('\n')


    # Classes that implement various approximate string matching algorithms
    approxAlgs = {}
    approxAlgs['neighbor'] = NeighborhoodSearch(dictionary, N_DIST)
    approxAlgs['nGram'] = GenericAlgorithm(dictionary)          #NgramDistance(dictionary)
    approxAlgs['globalEdit'] = GenericAlgorithm(dictionary)   #GlobalEditDistance(dictionary)

    for typo in misspell:
        typo = typo.strip('\n')

        for algorithm in approxAlgs:

            # Run the algorithms
            approxAlgs[algorithm].findCorrections(typo)

            approxAlgs[algorithm].stats['num_attempted'] += len(approxAlgs[algorithm].possibleSpellings[typo])

            try:
                # this will KeyError unless the correct spelling was found by the algorithm
                if approxAlgs[algorithm].possibleSpellings[typo][correctSpelling[typo]]:

                    if len(approxAlgs[algorithm].possibleSpellings[typo]) == 1:
                        approxAlgs[algorithm].stats['perfect_match'] += 1

                    else:
                        approxAlgs[algorithm].stats['match'] += 1

            except KeyError:
                # No match, check if there were no suggested corrections at all
                if len(approxAlgs[algorithm].possibleSpellings[typo]) == 0:
                    approxAlgs[algorithm].stats['no_match'] += 1

                # Otherwise some corrections were attempted, but none were the intended spelling
                else:
                    approxAlgs[algorithm].stats['incorrect'] += 1


    # print out results
    for algorithm in approxAlgs:
        print (approxAlgs[algorithm].stats)

