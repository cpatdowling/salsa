#Chase Dowling, June 2014, chase.dowling@pnnl.gov

#Using FFTW package for performing FFT on time series data, resovling
#phase angle, and dampening by a tunable factor alpha on the original
#time series in an attempt to eliminate periodic behavior.  Works for
#normalized and unormalized time series.

fftDampen <- function(inVector, paramF=param){
    transform = fft(inVector)
    movingAverage = rep(1/(as.integer(paramF$periodicWindow)), (as.integer(paramF$periodicWindow) + 1))
    complexAverage = complex(real=movingAverage, imaginary=movingAverage)
    convolution = complexFilter(transform, complexAverage, 2)
    return(convolution)
    #inverse is unormalized freq magnitude in C^1
    dampened = fft(convolution, inverse=TRUE) / length(inVector)
    #return(dampened)
}
