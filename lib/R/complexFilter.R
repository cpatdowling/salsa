#Chase Dowling, June 2014, chase.dowling@gmail.com 
#
#This function accepts a complex data vector and a complex filter vector
#and filters the two, performing complex arithmetic.

complexFilter <- function(inVector, filter, filterSize=2){
    outReal = filter(Re(inVector), Re(filter), sides=filterSize)
    outIm = filter(Im(inVector), filter, sides=filterSize)
    output = complex(real=outReal, imaginary=outIm)
    return(output)
    } 
