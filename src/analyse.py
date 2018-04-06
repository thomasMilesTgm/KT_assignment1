from cache import *

def analyse(params):

    dictFilepath = "../data_19mar/dictionary.txt"
    misspell = open("../data_19mar/misspell.txt",'r').readlines()
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
    approxAlgs = init_cache(params, dictionary)

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

    write_cache(approxAlgs, params)




if __name__=="__main__":


    param = {'NGram distance': 2, 'NGram threshold': 1, 'Neighborhood distance': 1, 'Metaphone neighbors': 1, 'Metaphone nGrams': 2, 'Metaphone nG threshold': 0.9}
    analyse(params=param)
