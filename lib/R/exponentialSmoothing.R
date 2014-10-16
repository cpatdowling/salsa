expSmooth<-function(inVector,maVector,sdVector,numHoursAhead){
	rawModel = ses(inVector, h=as.integer(numHoursAhead), level=80, fan=FALSE, initial="optimal", alpha=NULL, beta=NULL, gamma=NULL)
	#smoothModel = ses(maVector, h=as.integer(numHoursAhead), level=80, fan=FALSE, initial="optimal", alpha=NULL, beta=NULL, gamma=NULL)
	sdModel = ses(sdVector, h=as.integer(numHoursAhead), level=80, fan=FALSE, initial="optimal", alpha=NULL, beta=NULL, gamma=NULL)
	
	esDataDiff = inVector - rawModel$residuals
	esFit = cor(inVector, esDataDiff, use="complete.obs")^2
	
	sdDataDiff = sdVector - sdModel$residuals
	sdDataFit = cor(sdVector, sdDataDiff, use="complete.obs")^2
	#sdDataFit = "crap"
	
	#smoothDataDiff = maVector - smoothModel$residuals
	#smoothDataFit = cor(maVector, smoothModel$residuals, use="complete.obs")^2
	smoothDataFit = "crap"
	
	#esPred = predict(rawModel)
	#smoothPred = predict(smoothModel, n.ahead = as.integer(numHoursAhead))
	#sdPred = predict(sdModel, n.ahead = as.integer(numHoursAhead))
	
	NArawVector = rep("NA", length(inVector))
	NApredVector = rep("NA", as.integer(numHoursAhead))
		
	sdPredVector = c(c(NArawVector), c(c(sdModel$mean)))
	smoothPredVector = c(c(NArawVector), c(NApredVector))
	rawPredVector = c(c(NArawVector), c(c(rawModel$mean)))
	
	outRaw_frequency = c(inVector, c(NApredVector))
	outRaw_MA = c(c(maVector), c(NApredVector))
	outRaw_SD = c(c(sdVector), c(NApredVector))
	
	outTimeSeries = data.frame(raw_freq=outRaw_frequency, raw_MA=outRaw_MA, raw_SD=outRaw_SD, pred_freq=rawPredVector, pred_MA=smoothPredVector, pred_SD=sdPredVector)
		
	return(list(outTimeSeries, esFit, rawModel, sdDataFit, smoothDataFit))
	}
        