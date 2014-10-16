mFilter <- function(inVector){
        #Chase Dowling, last updated 4/22/2013, chase.dowling@pnnl.gov
        #This function accepts an input vector, assumed to be non-stationary, 
        #and applies the validate package function makeOutlierWeights() to cre-
        #ate appropriate m_estimation weights to correct  the importance of ou-
        #tlier values, and then returns the weighted data.  The input series is
        #first differenced, shifted one value to the right to account for the d
        #ifferencing, weighted, and then returned.  Can handle NA's.
        #
        #Futher, in order to account for the mFilter catching the differened d-
        #ata producing two spikes rather than 1, the original vector is revere-
        #sed, the processes rerun, and average of the two are taken.  This at  
        #least concentrates the effect of the filter on the outliers themselves
        #
        require(validate)
        
        if(mode(inVector)!="numeric"){
        	print("Input error in mFilter(), not of type 'numeric'")
        	stop()
        	}
        
        diffInputVector = diff(inVector)
        diffInputVector[is.na(diffInputVector)] = 0
        
        setParms() #required call under 'validate' package
        m_weights = makeOutlierWeights(diffInputVector)
        
        shiftedWeights = c(1.0, m_weights$outlier.weights)
        
        outVector = shiftedWeights * inVector
 
        return(outVector)
        }
