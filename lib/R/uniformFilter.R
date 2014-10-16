uniformFilter<-function(frequencyVector,maWindow){
        #function takes frequency vector, an even numbered window length 
	#requires caTools from the CRAN library--nonstandard packages
	#returns data.frame of raw_freq, raw_MA, raw_SD
	
	MA_coeff = rep(1/(as.integer(maWindow) + 1), (as.integer(maWindow) + 1))
	MA_sym = filter(frequencyVector, MA_coeff, sides=2)
	SD_sym = runsd(frequencyVector, (as.integer(maWindow) + 1), align = c("center"))
	
	outTimeSeries = data.frame(raw_freq=frequencyVector, raw_MA=MA_sym, raw_SD=SD_sym)
	return(list(outTimeSeries, summary(frequencyVector), summary(MA_sym), summary(SD_sym)))
	}
