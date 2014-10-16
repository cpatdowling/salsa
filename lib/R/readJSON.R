readJSON <- function(content) {
	#Chase Dowling, 09/03/2013, chase.dowling@pnnl.gov
	#
	#reads JSON dictionary and returns data frame with dates
	#as key values and time series values as hashed values
	#
	#content can either be a character vector of a filename address
	#or web address
	
	require(RJSONIO)
	
	variable = fromJSON(content, nullValue = NA)
	outputFrame = as.data.frame(variable)
        return(outputFrame)
	}
