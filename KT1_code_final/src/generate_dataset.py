from  multiprocessing import Process
from run_analysis import run
import sys
import os
from cache import clearCache
from utils import tex_tbl_end as end_tx
from psutil import virtual_memory
import time
"""Script that iterates through a wide range of parameters to generate data"""

def nGram_go():
    for i in range (1, 10):
        j = 1
        #for j in range(1,3):
        run(j, float(i)/10, 1, 1, 1, 1)

def mGram_go():
    for i in range (1, 10):
        for j in range(1,4):
            run(1, 1, 1, 1, j, float(i) / 10)

def nei_go():
    for j in range(1, 3):
        run(1, 1, j, 1, 1, 1)

def mei_go():
    for j in range(1, 3):
        run(1, 1, 1, j, 1, 1)


if __name__=='__main__':
    mem = virtual_memory()
    if mem.available < 40*pow(10,9):
        key = str(raw_input( "NOTE: this program is highly resource intensive!" 
              "\nIt is not recommended to run on a system with less than 40Gb available system memory.\nProceed? (Y/n): "))
        while key != 'Y':
            if key == 'n':
                sys.exit(0)
            else:
                os.system('clear')
                key = str(raw_input('Proceed? (Y/n): '))


    clearCache(False, True)
    run(1,1,1,1,1,1)    # run default values to save each process computing algorithms outside their scope

    p1 = Process(target=nGram_go)
    #p2 = Process(target=mGram_go())
    #p3 = Process(target=nei_go())
    #p4 = Process(target=mei_go())
    # for i in range (1, 10):
    #     for j in range(1,4):
    #         #p1 = Process(target=run, args= (j, float(i)/10, 1, 1, 1, 1)) # nGram
    #         p2 = Process(target=run, args=(1, 1, j, 1, 1, 1))            # neighborhood
    #         p3 = Process(target=run, args=(1, 1, 1, j, 1, 1))            # metaphone-neighborhood
    #         p4 = Process(target=run, args=(1, 1, 1, 1, j, float(i) / 10))# metaphone-ngram

    p1.start()

    #p2.start()
    # p3.start()
    #p4.start()
        # while p2.is_alive() and p3.is_alive() and p4.is_alive():
        #     time.sleep(1)


    end_tx()