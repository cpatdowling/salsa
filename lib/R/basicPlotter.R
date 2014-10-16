#reads a hard file and plots it

basicPlotter <- function(input, outputpath, title){

	args = commandArgs(trailingOnly = TRUE)
	argList = unlist(strsplit(args, split = " "))

	inputDir = input
	outputDir = outputpath
	cluster = title
	
	inputData = read.csv(inputDir, header = TRUE)

	jpeg(paste(outputDir, ".jpg", sep=""))
	#par(cex.axis = 1.2, cex.lab = 1.2, cex.main = 1.3, mfrow = c(1,6)) mfrow stacks images into one file

	plot(c(inputData$num_inf), type="l", xlab="Time Index--Hours", ylab="Feature Frequency", col="red", lwd=2)
	title(cluster)
	for (i in names(inputData)){
		lines(c(inputData$num_sus))
		}
	dev.off()
	}