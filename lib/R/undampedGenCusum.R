#Chase Dowling, chase.dowling@pnnl.gov, 5/5/2013
#
#Accepts a particular time series, determines a moving average with specified  
#filter distribution and two sided window length, and calculates the generaliz-
#ed cumulative sum for that time series.  The number of standard deviations fr-
#om the localized mean to detect a signal is given by the threshold parameter.
#reads parameters from salsa param object

undampedGenCusum <- function(inVector, paramF=param){
	#require(caTools)
	#require(monitoring)
	#require(pnlStat)
	
	window=paramF$window
    filter=as.character(paramF$filter)
    reference=as.integer(paramF$reference)
    control=as.integer(paramF$control)
    resetVal=as.integer(paramF$resetVal)
	smoothVector = movAvg2(inVector, bw=(window/2), type=filter)
	sdVector = runsd(inVector, (as.integer(window) + 1), align = c("center"))

	#normalizing time series with filtered data/standard deviation locally
	#determined by window length
	inVector_prime = (inVector - smoothVector)/sdVector
	inVector_prime[is.na(inVector_prime)] = 0
	inVector_prime[is.infinite(inVector_prime)] = 0
	
	cusum = calcCusum(inVector_prime, reference, control)

	return(cusum)
	}
