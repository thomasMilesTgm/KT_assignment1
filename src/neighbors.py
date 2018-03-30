import os
import re

lowerCase = "abcdefghijklmnopqrstuvwxyz"
upperCase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"

chars = lowerCase
DIST = 1

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

def processData():

    totalPerfect = 0
    totalPossible = 0
    totalWords = 0

    misspell = open("../data_19mar/misspell.txt",'r')
    dictFilepath  = "../data_19mar/dictionary.txt"
    output = open("../out/neighborhood_out.txt", "w")

    check = misspell.readlines()

    dict = {}
    for word in open(dictFilepath, 'r'):
        dict[word] = 1

    for word in check:
        numPossible = 0

        os.system('clear')
        print str(totalWords) + " Words have been checked"
        print str(totalPerfect) + " were perfect matches to a word in the dictionary"
        print str(totalPossible) + " possible alternate spelling have been found\n\n"

        totalWords += 1

        try:
            if dict[word]:

                totalPerfect += 1
                output.write(word.strip('\n') + ' 1\n')

        except KeyError, e:

                outputLine = "----"
                permute = neighbors(word, DIST)
                neighborMatch = False

                for permutation in permute:
                    try:
                        if dict[permutation]:

                            totalPossible += 1
                            numPossible += 1

                            if neighborMatch:
                                outputLine += ", " + permutation.strip('\n')

                            else:
                                outputLine = permutation.strip('\n')

                            neighborMatch = True

                    except KeyError, e:
                        pass

                output.write(outputLine + " " + str(numPossible) + '\n')

    output.close()
    misspell.close()

def compare():
    out = open('../out/neighborhood_out.txt', 'r').readlines()
    correct = open('../data_19mar/correct.txt', 'r').readlines()

    correctFound = 0
    noAttempt = 0
    noneCorrect = 0
    numGuesses = 0
    oneGuess = 0

    for i in range(0,len(out)):

        match = out[i]
        intended = correct[i]

        rxCorrect = '('+intended.strip('\n')+')'

        found = re.search(rxCorrect , match)
        if found:
            if re.search(' 1$', match):
                oneGuess += 1
                numGuesses += 1
            else:

                correctFound += 1
                if re.search('[2-9].$', match):
                    numGuesses += int(re.search('[2-9].$', match).group(0))

        else:

            if re.search(' 0$', match):
                noAttempt +=1

            else:
                noneCorrect +=1
                numGuesses += 1


    print    "Correct "+ str(correctFound)+ "\nPerfect "+str(oneGuess)+"\nNo Chance " +str(noAttempt)+"\nBad Guess " +str(noneCorrect)+ "\nGuesses " +str(numGuesses)

if __name__=="__main__":

    processData()
    compare()
