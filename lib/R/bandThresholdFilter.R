#Chase Dowling, June 2013, chase.dowling@pnnl.gov

#This function accepts a Fourier transformed signal, calculates
#the mean and standard deviation of all real components of the 
#frequencies of the original signal, and cuts off all frequencies
#above an input number of standard deviations, shifting the magnitude
#and factoring above zero to maintain original derivative signs.  
#
#Inputs: signal in frequency basis, number of standard deviations
#dampening factor

bandThresholdFilter <- function(inputVector, param){
    factor = param$fftDampenFactor
    threshold = param$fftThreshold
    convolution = fft(inputVector)
    inputReal = Re(convolution)
    inputComplex = Im(convolution)
    average = mean(inputReal)
    standev = sd(inputReal)
    threshValue = ( threshold * standev ) + average
    for (i in 1:length(inputVector)) {
        if (inputReal[[i]] > threshValue) {
            damp = factor*(inputReal[[i]] - threshValue)
            newReal = threshValue + damp
            ratio = newReal / inputReal[[i]]
            newComplex = ratio * inputComplex[[i]]
            inputReal[[i]] = newReal
            inputComplex[[i]] = newComplex 
        }
        if (inputReal[[i]] < -1 * threshValue) {
            damp = factor*(inputReal[[i]] + threshValue)
            newReal = threshValue + damp
            ratio = newReal / inputReal[[i]]
            newComplex = ratio * inputComplex[[i]]
            inputReal[[i]] = newReal
            inputComplex[[i]] = newComplex
        }
    }
    threshConvolution = complex(real=inputReal, imaginary=inputComplex)
    bandThresholded = abs(Re(fft(threshConvolution, inverse=TRUE) / length(inputVector)))
    return(bandThresholded)
}
