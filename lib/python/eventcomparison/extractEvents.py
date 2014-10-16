#Chase Dowling, chase.dowling@pnnl.gov, August 2014
#
#This class reads and parses events extracted by cusum
#for clustering by k-spectral centroid

import os
import json

class events:
    def __init__(self, dataDir="", outputDir="", win=8):
        self.window = win
        if dataDir == "":
            print("no data specified when class event was invoked")
            sys.exit()
        self.dataDirectory = dataDir
        if outputDir == "":
            self.outputDirectory = os.getcwd() + "/default_event_output"
        else:
            self.outputDirectory = outputDir
        if not os.path.exists(self.outputDirectory):
            os.mkdir(self.outputDirectory) 
    
    def parse_cusum_output(self):
        #in case there are unrelated reference files
        inFiles = [ inFile for inFile in os.listdir(self.dataDirectory) if inFile.split(".")[-1] == "json" ]
        for inFile in inFiles:
            inData = self.read_cusum_output(self.dataDirectory + "/" + inFile)
            parsed = self.get_events(inData, self.window)
            self.write_events_file(self.outputDirectory + "/" + inFile.rstrip(".json"), parsed)
            self.write_matlab_events_matrix(self.outputDirectory + "/" + inFile.rstrip(".json"), parsed)

    def read_cusum_output(self, filepath):
        print("parsing " + filepath)
        inFile = open(filepath, 'r')
        line = "".join([ linestring.strip() for linestring in inFile.readlines() ])
        inFile.close()
        data = json.loads(line)
        #keys = [u'date', u'inputSeries', u'cusumScore', u'eventCounter']
        return(data)

    def get_events(self, cusumFrame, window):
        outputData = {}
        index = 1
        for i in range(len(cusumFrame[u'date'])):
            if cusumFrame[u'eventCounter'][i] > index:
                index += 1
                try:
                    #skip events that occur at the very beginning and end--when window doesn't fit
                    appendData = [ str(item) for item in cusumFrame[u'inputSeries'][i-(window/2):i+(window/2)] ]
                    outputData[int(cusumFrame[u'date'][i])] = appendData
                except:
                    pass
            else:
                pass 
        return(outputData)

    def write_events_file(self, fileName, dataDict):
        print("writing " + fileName)
        #json dict, key is date of event, values are time series in a list
        outFile = open(fileName + "_events.json", 'w')
        out = json.dumps(dataDict)
        outFile.write(out)
        outFile.close()

    def write_matlab_events_matrix(self, fileName, dataDict):
        #each time series written as a row in a csv matrix file
        #writes reference file were each row is number corresponding to date
        outFile = open(fileName + "_events.csv", 'w')
        refFile = open(fileName + "_events_reference.csv", 'w')
        dates = sorted(dataDict.keys())
        for date in dates:
            outFile.write(",".join(dataDict[date]) + "\n")
            refFile.write(str(date) + "\n")
        outFile.close()
        refFile.close()
