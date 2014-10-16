#so really, the cusum isn't moving, but it's a cusum built for nonstationary, and probably not
#constant-variance time series.
#
#Chase Dowling, chase.dowling@pnnl.gov, 5/5/2013
#
#Accepts a particular time series, determines a moving average with specified  
#filter distribution and two sided window length, and calculates the generaliz-
#ed cumulative sum for that time series.  The number of standard deviations fr-
#om the localized mean to detect a signal is given by the threshold parameter.

dampedGenCusum <- function(inVector, param){
	#require(caTools)
	#require(monitoring)
	#require(pnlStat)
	
	#error handling for argument types here
	
	#controlling for outliers, applying an m-estimation filter to the differenced
	#series, and then choosing the max of the forward-backward applied filter for
	#each value to account for first differences values used to generate filter.
    reference = param$reference
    control = param$control
    resetVal = param$resetVal
    window = param$window
    filter = param$filter

	inVector[is.na(inVector)] = 0
	inVector[is.infinite(inVector)] = 0
	damped_series = c(mFilter(inVector))
	r_damped_series = c(mFilter(rev(inVector)))
	c_damped_series = rev(r_damped_series)
	m_series = pmax(r_damped_series, c_damped_series, na.rm=FALSE)
	
	smoothVector = movAvg2(inVector, bw=(window/2), type=filter)
	sdVector = runsd(inVector, (as.integer(window) + 1), align = c("center"))
	
	#normalizing time series with filtered data/standard deviation locally
	#determined by window length
	inVector_prime = (inVector - smoothVector)/sdVector
	inVector_prime[is.na(inVector_prime)] = 0
	inVector_prime[is.infinite(inVector_prime)] = 0
	
	cusum = calcCusum(inVector_prime, reference, control, initial = 0, type = "upper", reset = resetVal)

	return(cusum)
	}
