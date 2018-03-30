import os

out = open('../out/neighborhood_out.txt', 'r').readlines()
correct = open('../data_19mar/correct.txt', 'r').readlines()

numCorrect = 0
numAttempt = 0 # number of attempted corrections

for match in out:
    for intended in correct:

        rxCorrect = '^' + correct.strip('\n') + '$'
        if not os.system('grep '+rxCorrect + ' match'):
            # a correct spelling was found
            numCorrect += 1

        # this depends on correct formating of the output file
        # where the number at the end of each line specifies the
        # number of attempted corrections
        numAttempt += os.system('grep [0-9]$' + match)




