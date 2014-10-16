#Chase Dowling, chase.dowling@pnnl.gov, August 2014

#This is essentially the same script as /salsa/src/python/time_series_wrapper.py
#Working around the path recognition issue described there.

import sys
import os
import subprocess
from time import clock

#path to parameter file
paramLoc = sys.argv[1]

#path to input
inputDir = sys.argv[2]
      
#path to output
outputDir = sys.argv[3]

try:
    analyses = sys.argv[4]
except:
    pass

if not os.path.exists(outputDir):
    os.mkdir(outputDir)

#getting json files for analysis
inFiles = os.listdir(inputDir)
filesToRead = []
for file in inFiles:
    if file[len(file)-4:len(file)] == "json":
        filesToRead.append(inputDir + "/" + file)

for file in filesToRead:
    print("analyzing time series file: " + file)
    t1 = clock()
    subprocess.call("Rscript salsaBatchMode.R " + " -f -a U -i " + file + " -o " + outputDir + " -p " + paramLoc, shell=True)
    t2 = clock()
    print(file + " took " + str(t2-t1) + " seconds")
