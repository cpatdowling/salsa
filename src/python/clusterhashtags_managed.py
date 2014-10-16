#Chase Dowling, July 2014, chase.dowling@pnnl.gov
#
#This script accepts an input and output directory of files containing
#authors that use a given hashtag, distributes the clustering process across
#all available cpu's, and outputs their individual correlations. Once complete
#these files are compiled into a single correlation matrix as well as a text
#file showing clusters at a distance of .85

import os
import sys
import pathConfig
from hashtagclustering import clusterlib
from multiprocessing import Manager 
from multiprocessing import Pool

cores = sys.argv[1]

inputDir = sys.argv[2]
try:
    outDir = sys.argv[3]
except:
    outDir = ""

def poolworker_init(shared_data):
    poolworker.shared_data=shared_data

def poolworker(workitem):
    print("worker initialized on " + workitem)
    worker = clusterlib.clustering(dataDir=inputDir, outputDir=outDir)
    worker.correlate_single(workitem, poolworker.shared_data)
    return(True)

if __name__=="__main__":
    manager = Manager()
    shared = manager.dict()
    print(shared)
    allData = clusterlib.clustering(dataDir=inputDir, outputDir=outDir)
    allData.retrieveData()
    for key in allData.hashtagDict.keys():
        shared[key] = allData.hashtagDict[key]
    shared["number_of_authors"] = allData.numAuthors
    pool = Pool(processes=int(cores), initializer=poolworker_init, initargs=(shared,))
    tasks = pool.map_async(poolworker, allData.allHashtags)
    pool.close()
    pool.join()
    allData.compile_correlation_files()
    allData.cluster()
