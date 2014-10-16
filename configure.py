#Chase Dowling, 08/23/2013, chase.dowling@pnnl.gov
#
#This python script will configure and write pathConfig.R
#for salsa R scripts.  When installing salsa, run makeAll.py
#from the root /path/to/salsa directory.
#
#Will overwrite existing file for restructuring paths
#
#usage:
#python configure.py

import sys, os, subprocess

currentDir = os.getcwd()


system = "unix"
tokens = currentDir.split("/")
if tokens[len(tokens)-1] != "salsa":
	if currentDir.split("\\")[-1] == "salsa":
	#It's a windows system
		print("Windows operating system detected: WARNING--SALSA is tested and developed on UNIX platforms")
		system = "windows"
		lis = currentDir.split("\\")
		currentDir = "\\\\".join(lis)
	else:	
		print("Please re-run configure.py from ../../salsa directory\n...exiting")
		sys.exit()
print("Setting Salsa path: " + currentDir)

#writing package installer
header ="packageCheck <- function(update=FALSE, libraryLoc='"
body = "){\n\t#checks to make sure if required packages are installed and loads them\n\t#if update == TRUE, then packageCheck will find and download the newest\n\t#version of R--sadly this only works for windows\n\tif(!require('caTools', lib.loc=libraryLoc)){\n\t\tinstall.packages(\"caTools\", lib=libraryLoc, dep=TRUE, repos='http://ftp.osuosl.org/pub/cran/')\n\t\tlibrary('caTools', lib.loc=libraryLoc)\n\t\t}\n\tif(!require('RJSONIO', lib.loc=libraryLoc)){\n\t\tinstall.packages(\"RJSONIO\", lib=libraryLoc, dep=TRUE, repos='http://ftp.osuosl.org/pub/cran/')\n\t\tlibrary('RJSONIO', lib.loc=libraryLoc)\n\t\t}\n\tif(!require('pnlStat', lib=libraryLoc)){\n\t\tinstall.packages(\"pnlStat\", lib=libraryLoc, dep=TRUE, repos='http://martingale.pnl.gov/computing/repos/')\n\t\tlibrary('pnlStat', lib.loc=libraryLoc)\n\t\t}\n\tif(!require('monitoring', lib.loc=libraryLoc)){\n\t\tinstall.packages(\"monitoring\", lib=libraryLoc, dep=TRUE, repos='http://martingale.pnl.gov/computing/repos/')\n\t\tlibrary('monitoring', lib.loc=libraryLoc)\n\t\t}\n\tif(!require('ggplot2', lib.loc=libraryLoc)){\n\t\tinstall.packages(\"ggplot2\", lib=libraryLoc, dep=TRUE, repos='http://ftp.osuosl.org/pub/cran/')\n\t\tlibrary('ggplot2', lib.loc=libraryLoc)\n\t\t}\n\tif(!require('validate', lib.loc=libraryLoc)){\n\t\tinstall.packages(\"validate\", lib=libraryLoc, dep=TRUE, repos='http://martingale.pnl.gov/computing/repos/')\n\t\tlibrary('validate', lib.loc=libraryLoc)\n\t\t}\n\tif(update==TRUE){\n\t\tlibrary('installr', lib.loc=libraryLoc)\n\t\tupdateR()\n\t\tupdate.packages()\n\t\t}\n\treturn(libraryLoc)\n\t}"
  
print("Writing package installer: " + currentDir + "/lib/R/packageCheck.R")
if system == "unix":
    packageInstaller = open("lib/R/packageCheck.R", 'w')
    packageInstaller.write(header + currentDir + "/src/R/packages'")
    packageInstaller.write(body)
else:
    packageInstaller = open("lib\\R\\packageCheck.R", 'w')
    packageInstaller.write(header + currentDir + "\\\\src\\\\R\\\\packages'")
    packageInstaller.write(body)
packageInstaller.close()

#retrieving R and python lib functions
if system == "unix":
    Rfiles = os.listdir(currentDir + "/lib/R")
    pythonPackages = os.listdir(currentDir + "/lib/python")
else:
    Rfiles = os.listdir(currentDir + "\\lib\\R")
    pythonPackages = os.listdir(currentDir + "\\lib\\python")

#writing file depencies calls for R
print("Writing file dependencies to /salsa/src/R/pathConfig.R and /salsa/src/python/pathConfig.py")
if system == "unix":
    pathFile = open("src/R/pathConfig.R", 'w')
    pathFilePython = open("src/python/pathConfig.py", 'w')
else:
    pathFile = open("src\\R\\pathConfig.R", 'w')
    pathFilePython = open("src\\python\\pathConfig.py", 'w')


#Trying to write additional lib path here
pathFilePython.write("import sys\n\n")
pathFilePython.write("#This script is created at running of makeAll.py and picks up python packages for instances run from src directory\n\n")
if system == "unix":
    pathFilePython.write("sys.path.append(\"" + currentDir + "/lib/python\")\n")
    pathFilePython.write("sys.path.append(\"" + currentDir + "/src/R\")\n")
else:
    pathFilePython.write("sys.path.append(\"" + currentDir + "\\\\lib\\\\python\")\n")
    pathFilePython.write("sys.path.append(\"" + currentDir + "\\\\src\\\\R\")\n")

if system == "unix":
    for package in pythonPackages:
        print("including " + currentDir + "/lib/python/" + package)
else:
    for package in pythonPackages:
        print("including " + currentDir + "\\\\lib\\\\python" + package + " (windows)")
pathFilePython.close()

pathFile.write("pathConfig <- function(){\n\t#This function is created at running of makeAll.py and picks up all the R functions in ../salsa/lib\n")

print("including " + currentDir + "/lib/R")
for Rfile in Rfiles:
    if system == "unix":
        pathFile.write("\tsource(\"" + currentDir + "/lib/R/" + Rfile + "\")\n")
    else:
        pathFile.write("\tsource(\"" + currentDir + "\\\\lib\\\\R\\\\" + Rfile + "\")\n")
pathFile.write("\t}")
pathFile.close()

#writing environment build for R interactive and batch modes
print("Writing to Renviron.site RC type file for initializing salsaOnR")
if system == "unix":
	environFile = open("src/R/Renviron.site", 'w')
	environFile.write('R_PROFILE=\'' + currentDir + '/src/R/Rprofile.site\'\n')
else: 
	environFile = open("src\\R\\Renviron.site", 'w')
	environFile.write('R_PROFILE=\'' + currentDir + '\\\\src\\\\R\\\\Rprofile.site\'\n')	
environFile.close()

#writing init scripts for interactive/batch
if system == "unix":
	batchInit = open("src/R/salsaBatchInit.sh", 'w')
	batchInit.write("#!/bin/bash\nexport R_ENVIRON=" + currentDir + "/src/R/Renviron.site\n")
	batchInit.write("Rscript salsaBatchMode.R $@\n")
	batchInit.write("echo \"Runtime: $((enddate-startdate)) seconds.\"")
else:
	batchInit = open("src\\R\\salsaBatchInit.sh", 'w')
	batchInit.write("#!/bin/bash\nexport R_ENVIRON=" + currentDir + "\\\\src\\\\R\\\\Renviron.site\n")
	batchInit.write("Rscript salsaBatchMode.R $@\n")
	batchInit.write("echo \"Runtime: $((enddate-startdate)) seconds.\"")
batchInit.close()

if system == "unix":
	interactiveInit = open("src/R/interactiveInit.sh", 'w')
	interactiveInit.write("#!/bin/bash\nexport R_ENVIRON=" + currentDir + "/src/R/Renviron.site\n")
	interactiveInit.write("echo Initializing interactive session\n")
	interactiveInit.write("R\n")
else:
	interactiveInit = open("src\\R\\interactiveInit.sh", 'w')
	interactiveInit.write("#!/bin/bash\nexport R_ENVIRON=" + currentDir + "\\\\src\\\\R\\\\Renviron.site\n")
	interactiveInit.write("echo Initializing interactive session\n")
	interactiveInit.write("R\n")
interactiveInit.close()

print("configure complete")
