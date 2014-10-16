#Chase Dowling, 08/26/2013, chase.dowling@pnnl.gov
#
#setSalsaParms.R sets parameters for SALSA function calls,
#and should be used in each SALSA instance.
#
#filters may be: "uniform", "gaussian", "exponential", "linear"

setSalsaParms <- function(filterDef = "uniform", thresholdDef = 10, windowDef = 100, referenceDef = 0, controlDef = 1, resetValDef = 0, falseAlarmDef = 0.05, fftThresholdDef = 2, fftDampenFactorDef = .8){
	return(data.frame(filter=as.character(filterDef), threshold=as.single(as.character(thresholdDef)), window=as.single(as.character(windowDef)), reference=as.numeric(as.character(referenceDef)), control=as.numeric(as.character(controlDef)), resetVal=as.numeric(as.character(resetValDef)), falseAlarm=as.numeric(as.character(falseAlarmDef)), fftThreshold=as.single(fftThresholdDef), fftDampenFactor=as.single(fftDampenFactorDef)))
	}
