outputJSON <- function(dataFrame) {
	#Chase Dowling, 09/24/2013, chase.dowling@pnnl.gov
	#
	#reads R data frame and returns salsa JSON object
	
        header = names(dataFrame)[-1]
        newObj = setNames(data.frame(t(dataFrame[,-1])), dataFrame[,1])
        dateHeader = names(newObj)
        newObj$date = header
        newObj = newObj[c('date', dateHeader)]
        returnObj = toJSON(newObj)
        
        return(returnObj)
        }