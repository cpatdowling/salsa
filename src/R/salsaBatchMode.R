#Chase Dowling, 09/05/2013, chase.dowling@pnnl.gov
#
#salsaBatchMode.R is designed to accept and return JSON formatted data for web
#based services in the analysis of noisy, web data time series.  Accepts arbit-
#trary time series in JSON format described in ~/readme.txt with examples found
#in ~/test/testJSONTS.json
#
#This script is called in batch mode from the ~/src/R directory where the Rp-
#rofile.site, R.environ, and RData files are used to initialize a virtu-
#al R session with all default parameter values and libraries loaded.  This has
#only been written and tested on UNIX platforms.
#
#Command line args:
#
#	-a	JSON format array of strings specifying desired analyses to be
#		performed or character string of analyses or series of charac-
#               ters cooresponding to analytics: see primary documentation
#		(defaults to heurstic/cusum event detection analyses)
#	-p	JSON format hashmap of parameters to change from defaults
#		(Note: useflag -pc for generic csv input to R data.frame inste-
#		ad of JSON object)
#		(optional)
#	-i	path, string, or url to input JSON object.  String quotations 
#               must be escaped, i.e. column headers
#		(Note: use flag -ic for generic csv input instead of JSON)
#	-o	path to output location*, can use "STDOUT" for after -o flag.
#               (Note: use flag -oc for generic csv output instead of JSON)
#   -f  frequency flag, if found, FFT component waveforms are damped by a 
#       specified factor, defaulting to .8, also current defaulting to wav-
#       forms above 2 std of the mean waveform in the real component of 
#       the FFT transformed data
#Example usage:
#
#R CMD BATCH salsaBatchMode.R -a /path/or/url/to/json/analytics/libraryd -i /p-
#ath/or/url/to/json -o /path/to/output
#
#Warnings:
#
#This has only been tested for UNIX based OS's.  And never use the command line
#arg '-z'

args = commandArgs(trailingOnly = TRUE)
argList = unlist(strsplit(args, split = " "))

#path configuration
source("pathConfig.R")
pathConfig()
libraryLoc = packageCheck()

#Defaults
outputLocation = getwd()
outCSV = FALSE
inputLocation = "NULL"
inCSV = FALSE
newParameters = "NULL"
analyses = "G"
param = setSalsaParms()
periodic = FALSE

pathConfig()


i=1
while(i<=length(argList)){
	if(argList[[i]]=="-i"){
		inputLocation = argList[[i+1]]
		}
	if(argList[[i]]=="-ic"){
		inputLocation = argList[[i+1]]
		inCSV = TRUE
		}
    if(argList[[i]]=="-o"){
        outputLocation = argList[[i+1]]
        }
	if(argList[[i]]=="-oc"){
		outputLocation = argList[[i+1]]
		outCSV = TRUE
		}
    if(argList[[i]]=="-a"){
        analyses = argList[[i+1]]
        }
    if(argList[[i]]=="-p"){
        newParameters = argList[[i+1]]
        }
    if(argList[[i]]=="-f"){
        periodic = TRUE
        }
    if(argList[[i]]=="-z"){
        cat("All your base are now belong to me because you used -z.\n")
        }
        i=i+1
    }

#checking for input data        
if(inputLocation == "NULL"){
	stop("No input data specified--exiting")
	}
if(inCSV==TRUE){
	tsFrame = read.table(inputLocation, sep=",")
	} else {
    #variable = fromJSON(inputLocation, nullValue = NA)
    #tsFrame = as.data.frame(variable)
	tsFrame = readJSON(inputLocation)
	}

#reading requested analyses
if(length(strsplit(analyses,split="/")[[1]])>1){
	#NEEDS double quotes in array
	#>x <- fromJSON('["A", "B", "C"]')
	#[1] "A" "B" "C"
	analysesList = fromJSON(analyses)
	} else {
	analysesList = strsplit(analyses,split="")[[1]]
	}

#checking for non-default parameter specification
if(newParameters!="NULL"){
	newParam = readJSON(newParameters)
	newParamNames = names(newParam)
	z=1
	while(z<=ncol(newParam)){
		paramName = newParamNames[[z]]
		paramValue = newParam[1,z]
		param[,names(param) == paramName] = paramValue
		z=z+1
		}
        #cleaning up type problems in salsa param object
        #setSalsaParms does some coercion gymnastics around problems caused by
        #reading JSON objects in R like single quote v. double quote problem
	    print("new parameters detected")
        print(param)
    }

#loading libraries
suppressMessages(library('pnlStat', lib.loc=libraryLoc, quietly=TRUE))
suppressMessages(library('caTools', lib.loc=libraryLoc, quietly=TRUE))
suppressMessages(library('validate', lib.loc=libraryLoc, quietly=TRUE))
suppressMessages(library('monitoring', lib.loc=libraryLoc, quietly=TRUE))

#perform analyses
series = names(tsFrame)
b = 2  #skipping tsFrame$date column
while(b<=length(series)){
	inputVector = c(tsFrame[, names(tsFrame) == series[[b]]])
	print(paste("analyzing ", series[[b]], sep=""))
	if(is.vector(inputVector)==FALSE){
		stop("Houston, we have a problem: unable to correctly read input time series.")
		geterrmessage()
		}
    #If the analyst suspects the data is periodic--returns band rejected data 
    if(periodic==TRUE){
        inputVector = bandThresholdFilter(inputVector, param)
        }
	j=1
	outAnalyses = list()
	while(j<=length(analysesList)){
		if(analysesList[[j]]=="G"){
			smoothVector = dampedGenCusum(inputVector, param)
			outputFrame = data.frame(date=tsFrame$date, inputSeries=inputVector, cusumScore=smoothVector$cusum, eventCounter=smoothVector$resetCounter)
			}
		if(analysesList[[j]]=="U"){
			smoothVector = undampedGenCusum(inputVector, param)
			print(smoothVector)
            outputFrame = data.frame(date=tsFrame$date, inputSeries=inputVector, cusumScore=smoothVector$cusum, eventCounter=smoothVector$resetCounter)
			}
		if(analysesList[[j]]=="M"){
			smoothVector = mFilter(inputVector)
            outputFrame = data.frame(date=tsFrame$date, inputSeries=inputVector, outlierDampWeights=smoothVector)
			}
		if(analysesList[[j]]=="F"){
            dataVectors = runHeuristic(inputVector, param)
			outputFrame = data.frame(date=tsFrame$date, inputSeries=inputVector, smoothSeries=dataVectors$smoothVector, sdSeries=dataVectors$sdVector, eventCounter=dataVectors$eventCounter)
			}
		if(outCSV==TRUE){
			write.csv(outputFrame, file=paste(paste(paste(paste(outputLocation, "/", sep=""), series[[b]], sep=""), analysesList[[j]], sep="_"), ".json", sep=""), append = FALSE, quote = TRUE, row.names=FALSE, col.names=TRUE)
			}
        if(outputLocation=="STDOUT"){
            print(toJSON(outputFrame))
            }  else {
		cat(toJSON(outputFrame), file=paste(paste(paste(paste(outputLocation, "/", sep=""), series[[b]], sep=""), analysesList[[j]], sep="_"), ".json", sep=""))
			}
		j=j+1
		}
	b = b+1
	}

