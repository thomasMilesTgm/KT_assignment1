from GenericAlgorithm import *
from neighbors import NeighborhoodSearch
from ngram_distance import NgramAlgorithm
from datetime import datetime
from phonetic import *
from combined import *

CLEAR_CACHE = True

def analyse(params):

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

    # define the set of intended spellings
    for i in range(0, len(misspell)):
        correctSpelling[misspell[i].strip('\n')] = correct[i].strip('\n')

    # Classes that implement various approximate string matching algorithms
    approxAlgs = {}

    approxAlgs['neighbor'] = NeighborhoodSearch(dictionary, params['Neighborhood distance'])
    approxAlgs['nGram'] = NgramAlgorithm(dictionary, N=params['NGram distance'], match_threshold=params['NGram threshold'])
    approxAlgs['phonetic'] = Metaphone(dictionary)
    approxAlgs['exact only'] = GenericAlgorithm(dictionary)
    approxAlgs['metaphone-ngram'] = metaphone_ngram(dictionary, params['Metaphone nGrams'], match_threshold=params['Metaphone nG threshold'])
    approxAlgs['metaphone-neighborhood'] = metaphone_ngram(dictionary, params['Metaphone neighbors'])


    for typo in misspell:
        typo = typo.strip('\n')

        for algorithm in approxAlgs:

            # Run the algorithms
            approxAlgs[algorithm].findCorrections(typo)


            # evaluate statistics
            approxAlgs[algorithm].stats['num_attempted'] += len(approxAlgs[algorithm].possibleSpellings[typo])

            try:
                # this will KeyError unless the correct spelling was found by the algorithm
                if approxAlgs[algorithm].possibleSpellings[typo][correctSpelling[typo]]:

                    approxAlgs[algorithm].stats['match'] += 1

                    if len(approxAlgs[algorithm].possibleSpellings[typo]) == 1:
                        approxAlgs[algorithm].stats['perfect_match'] += 1



            except KeyError:
                approxAlgs[algorithm].stats['incorrect'] += 1

            # compute evaluation values
            if approxAlgs[algorithm].stats['num_attempted'] != 0:
                precision = float(approxAlgs[algorithm].stats['match'])/ approxAlgs[algorithm].stats['num_attempted']
                approxAlgs[algorithm].evaluation['precision'] = precision

            if (approxAlgs[algorithm].stats['match'] + approxAlgs[algorithm].stats['incorrect']) != 0:
                recall = float(approxAlgs[algorithm].stats['match'])\
                           / (approxAlgs[algorithm].stats['match'] + approxAlgs[algorithm].stats['incorrect'])
                approxAlgs[algorithm].evaluation['recall'] = recall

            if (approxAlgs[algorithm].stats['match'] + approxAlgs[algorithm].stats['incorrect']) != 0:
                accuracy = float(approxAlgs[algorithm].stats['perfect_match'])\
                           / (approxAlgs[algorithm].stats['match'] + approxAlgs[algorithm].stats['incorrect'])
                approxAlgs[algorithm].evaluation['accuracy'] = accuracy

    cache = open('../out/cache.txt', 'a')
    cache.write('\n' + str(datetime.now())+'\n')


    # cache and print results
    for algorithm in approxAlgs:

        string = approxAlgs[algorithm].name + '\n'

        if approxAlgs[algorithm].name == 'Neighborhood Distance':
            string += '{Neighborhood distance: ' + str(param['Neighborhood distance']) + '}\n'

        elif approxAlgs[algorithm].name == 'NGram Distance':
            string += '{nGram distance: ' + str(param['NGram distance']) + '}  {Threshold: ' + str(param['NGram threshold']) + '}\n'

        elif approxAlgs[algorithm].name == 'Metaphone-nGram':
            string += '{nGram distance: ' + str(param['Metaphone nGrams']) + '}  {Threshold: ' + str(param['Metaphone nG threshold']) + '}\n'

        elif approxAlgs[algorithm].name == 'Metaphone-neighborhood':
            string += '{Neighborhood distance: ' + str(param['Metaphone neighbors']) + '}\n'


        string += str(approxAlgs[algorithm].evaluation) + '\n' + str(approxAlgs[algorithm].stats) + "\n\n"

        cache.write(string)
        print (string)


if __name__=="__main__":

    if CLEAR_CACHE:
        cache = open('../out/cache.txt', 'w')
        cache.close()
    param = {'NGram distance': 2, 'NGram threshold': 0, 'Neighborhood distance': 1, 'Metaphone neighbors': 1, 'Metaphone nGrams': 2, 'Metaphone nG threshold': 0.9}
    analyse(params=param)

