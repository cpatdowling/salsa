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
#
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

#Defaults
outputLocation = getwd()
outCSV = FALSE
inputLocation = "NULL"
inCSV = FALSE
newParameters = "NULL"
analyses = "UF"
source("packageCheck.R")
libraryLoc = "windows_packages"
packageCheck(libLocation=libraryLoc)
source("pathConfig.R")
pathConfig()
param = setSalsaParms()

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
        if(argList[[i]]=="-z"){
                cat("All your base are now belong to me, lulz\n")
                cat("...\n")
                cat("But seriously, job will continue normally\n")
                cat("...\n")
                cat("...probably\n")
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
	while(z<=nrow(newParam)){
		paramName = newParam[z,1]
		paramValue = newParam[z,2]
		param[,names(param) == paramName] = paramValue
		z=z+1
		}
	}
	


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
	j=1
	outAnalyses = list()
	while(j<=length(analysesList)){
		if(analysesList[[j]]=="G"){
                        suppressMessages(library('pnlStat', lib.loc=libraryLoc, quietly=TRUE))
			suppressMessages(library('validate', lib.loc=libraryLoc, quietly=TRUE))
			suppressMessages(library('monitoring', lib.loc=libraryLoc, quietly=TRUE))
			suppressMessages(library('caTools', lib.loc=libraryLoc, quietly=TRUE))
			smoothVector = dampedGenCusum(inputVector, as.numeric(as.character(param$reference)), as.single(as.character(param$threshold)), as.numeric(as.character(param$resetVal)), as.numeric(as.character(param$window)), as.character(param$filter))
			outputFrame = data.frame(date=tsFrame$date, inputSeries=inputVector, cusumScore=smoothVector$cusum, eventCounter=smoothVector$resetCounter)
			}
		if(analysesList[[j]]=="U"){
                        suppressMessages(library('pnlStat', lib.loc=libraryLoc, quietly=TRUE))
			suppressMessages(library('monitoring', lib.loc=libraryLoc, quietly=TRUE))
			suppressMessages(library('caTools', lib.loc=libraryLoc, quietly=TRUE))
			smoothVector = undampedGenCusum(inputVector, as.numeric(as.character(param$reference)), as.single(as.character(param$threshold)), as.numeric(as.character(param$resetVal)), as.numeric(as.character(param$window)), as.character(param$filter))
			outputFrame = data.frame(date=tsFrame$date, inputSeries=inputVector, cusumScore=smoothVector$cusum, eventCounter=smoothVector$resetCounter)
			}
		if(analysesList[[j]]=="M"){
                        suppressMessages(library('pnlStat', lib.loc=libraryLoc, quietly=TRUE))
			suppressMessages(library('validate', lib.loc=libraryLoc, quietly=TRUE))
			suppressMessages(library('monitoring', lib.loc=libraryLoc, quietly=TRUE))
			smoothVector = mFilter(inputVector)
                        outputFrame = data.frame(date=tsFrame$date, inputSeries=inputVector, outlierDampWeights=smoothVector)
			}
		if(analysesList[[j]]=="E"){
                        suppressMessages(library('pnlStat', lib.loc=libraryLoc, quietly=TRUE))
			suppressMessages(library('caTools', lib.loc=libraryLoc, quietly=TRUE))
			suppressMessages(library('forecast', lib.loc=libraryLoc, quietly=TRUE))
			smoothVector = movAvg2(inputVector, bw=(as.numeric(as.character(param$window))/2), type=as.character(param$filter))
			sdVector = runsd(inputVector, (as.numeric(as.character(param$window)) + 1), align = c("center"))
			modelAndFit = expSmooth(inputVector, smoothVector, sdVector, as.numeric(as.character(param$nAhead)))
			outputFrame = data.frame(date=tsFrame$date, inputSeries=modelAndFit[[1]]$raw_freq, predictedSeries=modelAndFit[[1]]$pred_freq)
			}
		if(analysesList[[j]]=="F"){
                        suppressMessages(library('pnlStat', lib.loc=libraryLoc, quietly=TRUE))
			suppressMessages(library('caTools', lib.loc=libraryLoc, quietly=TRUE))
			smoothVector = movAvg2(inputVector, bw=(as.numeric(as.character(param$window))/2), type=as.character(param$filter))
			sdVector = runsd(inputVector, (as.numeric(as.character(param$window)) + 1), align = c("center"))
			maTextOutput = c(summary(inputVector), summary(smoothVector), summary(sdVector))
			eventCounter = 1
			eventVector = c()
			for (i in 1:length(inputVector)){
				if (as.single(as.character(param$reference))*sdVector[[i]] + smoothVector[[i]] < inputVector[[i]]){
					eventCounter = eventCounter + 1
					eventVector = c(eventVector, eventCounter)
					} else {
					eventVector = c(eventVector, eventCounter)
					}
				}
			outputFrame = data.frame(date=tsFrame$date, inputSeries=inputVector, smoothSeries=smoothVector, sdSeries=sdVector, eventCounter=eventVector)
			}
		if(analysesList[[j]]=="A"){
			#issue with passing/returning nAhead correctly
                        suppressMessages(library('pnlStat', lib.loc=libraryLoc, quietly=TRUE))
			suppressMessages(library('caTools', lib.loc=libraryLoc, quietly=TRUE))
			suppressMessages(library('forecast', lib.loc=libraryLoc, quietly=TRUE))
			smoothVector = movAvg2(inputVector, bw=(as.numeric(as.character(param$window))/2), type=as.character(param$filter))
			sdVector = runsd(inputVector, (as.numeric(as.character(param$window)) + 1), align = c("center"))
			xregger = "NULL"
			periodicity = "NULL"
     			modelAndFit = smoothARIMA(inputVector, smoothVector, sdVector, periodicity, xregger, param$nAhead)
     			outputFrame = data.frame(date=c(tsFrame$date, rep(NA, as.numeric(as.character(param$nAhead)))), inputSeries=modelAndFit[[1]]$raw_freq, predSeries=modelAndFit[[1]]$pred_freq)
			}
		if(outCSV==TRUE){
			write.csv(outputFrame, file=paste(paste(paste(paste(outputLocation, "/", sep=""), series[[b]], sep=""), analysesList[[j]], sep="_"), ".json", sep=""), append = FALSE, quote = TRUE, row.names=FALSE, col.names=TRUE)
			}
                if(outputLocation=="STDOUT"){
                        print(outputJSON(outputFrame))
                        }  else {
			cat(outputJSON(outputFrame), file=paste(paste(paste(paste(outputLocation, "/", sep=""), series[[b]], sep=""), analysesList[[j]], sep="_"), ".json", sep=""))
			}
		j=j+1
		}
	b = b+1
	}

