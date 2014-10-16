#Chase Dowling, chase.dowling@pnnl.gov, 11/15/2013
#
#Accepts a particular time series, determines a centered moving average and associated
#moving standard deviation.  For each raw input value, this function tests to see if 
#it is greater than a reference number of standard deviations greater than the moving
#average value at that point.  The window parameter drawn from the salsa param object
#determines what weights are used in calculated the moving average: a uniform filter
#being a moving average in the strictest sense.

runHeuristic <- function(inVector, paramF=param){
        require(caTools)
        require(pnlStat)
        
        window=paramF$window
        filter=as.character(param$filter)
        reference=paramF$reference
        
        smoothVector = movAvg2(inVector, bw=window/2, type=filter)
        sdVector = runsd(inVector, window + 1, align=c("center"))
        eventCounter = 1
        eventVector = c()
        for (i in 1: length(inVector)){
            if(param$reference*sdVector[[i]] + smoothVector[[i]] < inVector[[i]]){
                eventCounter = eventCounter + 1
                eventVector = c(eventVector, eventCounter)
                } else {
                eventVector = c(eventVector, eventCounter)
                }
        }
        
        outputFrame = data.frame(inputVector=inVector, smoothVector=smoothVector, sdVector=sdVector, eventCounter=eventVector)
        return(outputFrame)
        }
