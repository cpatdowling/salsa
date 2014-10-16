extractEventsHourly <- function(originalDates, cusumDataFrame) {
	eventCounter = 0
	dates = c()
	for(i in 1:length(originalDates)){
		if(cusumDataFrame$eventCounter[[i]] > eventCounter){
			dates = c(dates, originalDates[[i]])
            eventCounter = eventCounter + 1
			}
		}
	return(dates)
	}
