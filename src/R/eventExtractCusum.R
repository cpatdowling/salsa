#Chase Dowling, chase.dowling@pnnl.gov 5/5/2013
#
#Script that accepts a time series file, window length, and reference value and
#performs the genCusum.R function, and outputs a data.frame csv with the index,
#raw_freq, movAvg2 as raw_ma, either gaussian or uniform, and the cusum as thr-
#ee colums.
#
#Rscript /mnt/some/dowling/SIR_Simulation/R/eventExtractCusum.R --args path/to/time/s-
#eries /path/to/output window reference control filter
#
#
library(caTools)
library(monitoring)
library(pnlStat)
library(validate)
source("/mnt/some/dowling/SIR_Simulation/R/genCusum.R")
source("/mnt/some/dowling/SIR_Simulation/R/mFilter.R")

args = commandArgs(trailingOnly = TRUE)
argList = unlist(strsplit(args, split = " "))

print("reading arguments...")

inputDir = argList[[2]]
outputDir = argList[[3]]
window = argList[[4]]
reference = argList[[5]]
control = argList[[6]]
filter = argList[[7]]

print(c("reading data from:",inputDir))

inputTimeSeries = read.csv(inputDir, header=TRUE)
inputVector = c(inputTimeSeries$Frequencies)
if(length(inputVector)==0){
        inputVector = c(inputTimeSeries$Frequency)
}

smoothVector = movAvg2(inputVector, bw=((as.integer(window))/2), type = filter)

#genCusum(inVector, reference, control, resetVal, window, filter) --> $cusum $resetCounter
cusumVector = genCusum(inputVector, as.integer(reference), as.integer(control), TRUE, as.integer(window), filter)

outputFrame = data.frame(raw_freq=inputVector, raw_MA=smoothVector, cusum=cusumVector$cusum, event_count=cusumVector$resetCounter)

write.table(outputFrame, file=outputDir, row.names=T, sep=',', quote=F, col.names=c("raw_freq", "raw_MA", "cusum", "event_count"), eol="\n")