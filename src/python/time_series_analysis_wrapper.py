#Chase Dowling, chase.dowling@pnnl.gov, August 2014
#
#This wrapper launches time series analysis jobs on multiple
#json files created by the aggregate_ts.py script.

#***CURRENT ISSUE***
#salsaBatchMode.R requires the adjacent file pathConfig.R--the shell
#this script spawns spawns wherever this python script is invoked, so
#if pathConfig.R isn't in that directory, you're no better off than
#just using the bash init file in /salsa/src/R
#
#I apologize to the software engineer that has to take this over from me

import sys
import os
import subprocess
from time import clock

import pathConfig

#path to parameter file
paramLoc = sys.argv[1]

#path to input
inputDir = sys.argv[2]

#path to output
outputDir = sys.argv[3]

try: 
    sys.argv[4]
    #do a different kind of analysis
except:
    pass

if not os.path.exists(outputDir):
    os.mkdir(outputDir)

#pathConfig includes the R source directory as last list member although
#there is no python in that directory

RbatchInit = sys.path[-1] + "/salsaBatchMode.R"

#getting json files for analysis
inFiles = os.listdir(inputDir)
filesToRead = []
for file in inFiles:
    if file[len(file)-4:len(file)] == "json":
        filesToRead.append(inputDir + "/" + file)

for file in filesToRead:
    print("analyzing time series file: " + file)
    t1 = clock()
    subprocess.call("Rscript " + RbatchInit + " -f -i " + file + " -o " + outputDir + " -p " + paramLoc, shell=True)
    t2 = clock()
    print(file + " took " + str(t2-t1) + " seconds")
