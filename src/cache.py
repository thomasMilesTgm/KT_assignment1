from datetime import datetime
from algorithms import *
import os


param_cache = ['nei', 'ng', 'ngm', 'nem', 'meta']
param_converter = {'nei': ['Neighborhood distance'], 'ng': ['NGram distance', 'NGram threshold'],
                   'ngm': ['Metaphone nG threshold', 'Metaphone nGrams'], 'nem': ['Metaphone neighbors'],
                   'meta': []}

CLEAR_CACHE = True


def init_cache(params, dictionary):

    if CLEAR_CACHE:
        key = str(raw_input("WARNING: CLEAR_CACHE is True...\nAre you sure you want this? (Y/n)\n"))
        while key != 'Y' and key != 'n':
            os.system('clear')
            key = str(raw_input("Clear cache? (Y/n)\n"))

        if key == 'Y':
            os.system('rm -r ../out/* ../log/*')
            param_log = []
            for name in param_cache:
                param_log.append(open('../log/' + name, 'w'))

            for doc in param_log:
                doc.close()
        else:
            pass

    param_log = {}
    approxAlgs = {}

    for name in param_cache:
        param_log[name] = open('../log/' + name, 'r')

    # approxAlgs['exact only'] = GenericAlgorithm(dictionary)
    factory = AlgoFactory(dictionary, params)

    parsed = ''
    cached = False
    for name in param_cache:
        for line in param_log[name].readlines():
            for param in param_converter[name]:
                parsed += str(params[param])
            if parsed == line.strip('\n'):
                cached = True
                break

        if not cached:
            approxAlgs[name] = factory.getAlgo(name)

    return approxAlgs


def write_cache(approxAlgs, params):

    param_log = {}
    cache = open('../out/cache.txt', 'a')

    for name in param_cache:
        param_log[name] = open('../log/' + name, 'a')

    # cache and print results human readable
    # write logs
    log = ''
    for name in param_cache:
        for param in param_converter[name]:
            log += str(params[param])
        log += '\n'
        param_log[name].write(log)

    # write and print human readable cache
    cache.write('\n' + str(datetime.now())+'\n')

    for name in param_cache:
        string = approxAlgs[name].name + '\n'
        for param in param_converter[name]:
            string += '{ ' + str(param) + ' ' + str(params[param]) + ' }\n'

        string += str(approxAlgs[name].evaluation) + '\n' + str(approxAlgs[name].stats) + "\n\n"

        cache.write(string)
        print (string)