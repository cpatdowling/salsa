#Chase Dowling, chase.dowling@pnnl.gov, June 2014
#this functions accepts a stationary vector and returns weights
#for dampening outliers outside the 25th and 75th percentiles.

import numpy

def mFilter(inVector, trimFactor):
    inVector = numpy.asarray(inVector)

    #calculating trimmed mean and std
    trim = numpy.percentile(inVector, [25, 75])
    mean = numpy.average(inVector)
    xout_trim = list()
    for i in range(len(inVector)):
        if inVector[i] > trim[0] and inVector[i] < trim[1]:
            xout_trim.append(inVector[i])
    xout_trim = numpy.array(xout_trim)
    xout_mean = numpy.average(xout_trim)

    #calculate initial standardized values
    z = (inVector - xout_mean)/(numpy.std(xout_trim))
    z_cut = z
    while i < len(z_cut):
        try:
            if numpy.abs(z_cut[i]) > 50:
                numpy.delete(z_cut, i)
            i += 1
        except:
            print("out of bounds error function mFilter.py; will continue")
            i += 1
    
    #calculating cutoff range
    z_quantiles = numpy.percentile(z_cut, [25, 75])
    z_upper_cutoff = z_quantiles[1]
    z_lower_cutoff = z_quantiles[0]
    cutoff_range = z_upper_cutoff - z_lower_cutoff
    
    #scaling factor to make the outlier weights equal to 0.05 at 
    #cutoff_range * trimFactor units away from upper and lower cutoffs
    o_sigma_sq = (-(numpy.power(cutoff_range*trimFactor,2)))/(2*numpy.log(0.05))

    outlier_weights = numpy.array([1]*len(inVector))
    for i in range(len(outlier_weights)):
        if z[i] < z_lower_cutoff:
            z[i] = numpy.exp(-0.5*numpy.power((z[i] - z_lower_cutoff),2)) / o_sigma_sq
        if z[i] > z_upper_cutoff:
            z[i] = numpy.exp(-0.5*numpy.power((z[i] - z_upper_cutoff),2)) / o_sigma_sq

    return(z)
