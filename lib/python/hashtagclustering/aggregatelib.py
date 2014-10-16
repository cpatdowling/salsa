#Chase Dowling, July 2014, chase.dowling@pnnl.gov
#
#This library creates SALSA formatted time sereis with UNIX standard
#date-time strings from csv and serialized pickle files in the same csv
#format.
#
#Given the output of hashtag clustering, this class instance will read
#hashtag clusters and compiled SALSA formatted time series and output
#SALSA formatted time series for multiple series

import cPickle
import csv
import os
import sys
import datetime

class aggregate:
    def __init__(self, workingDir="", outputDir=""):
        #fully qualified paths in case output different than working
        if outputDir == "":
            self.outputDirectory = os.getcwd() + "/default_output_aggregate"
            if not os.path.exists(self.outputDirectory):
                os.mkdir(self.outputDirectory)
        else:
            self.outputDirectory = outputDir
            if not os.path.exists(self.outputDirectory):
                os.mkdir(self.outputDirectory)
        self.progressFile = self.outputDirectory + "/aggregate_log.txt"
        self.workingDirectory = workingDir
        file = open(self.progressFile, 'w')
        file.close()

    #def format_time_series(self, timeSeriesDict):
        #Converts the time series dict of date key, frequency value to a 
        #salsa formatted json object
        
    def retrieve_series_data(self, timeSeriesDir, fileIdentifiers="", extension="csv", delim="", header=False):
        if extension[0] != ".":
            extension = "." + extension
        self.timeSeries = dict()
        #timeSeriesDir needs leading "/" for fully qualified path *or* for relative path with defined self.workingDirectory
        for rank in self.clusters.keys():
            if rank not in self.timeSeries.keys():
                self.timeSeries[rank] = dict()
            for hashtag in self.clusters[rank]:
                #work around for josh's data
                hashtag = hashtag.rstrip(".author")
                try:
                    inFile = open(self.workingDirectory + timeSeriesDir + "/" + hashtag + fileIdentifiers + extension, 'r')
                    if extension == ".pck" or extension == ".pickle":
                    #files are serialized dictionaries, key = date, value = frequency
                        inData = cPickle.load(inFile)
                    elif extension == ".json":
                        #json formatted to salsa specification
                        print("no json extensibility in aggregate class")
                    elif extension == ".csv":
                        inLines = inFile.readlines()
                        if header == True:
                            inLines.remove(inLines[0])
                        for line in inLines:
                            tokens = line.strip().split(delim)
                            inData[tokens[0]] = int(tokens[1])
                    else:
                        print("bad file extension reading time series: " + extension)
                    try:
                        self.timeSeries[rank] = dict((n, self.timeSeries[rank].get(n, 0) + inData.get(n, 0)) for n in set(self.timeSeries[rank])|set(inData) )
                    except:
                        print("no data was read from file: " + self.workingDirectory + timeSeriesDir + "/" + hashtag + fileIdentifiers + extension)
                except:
                    print("error occured when attempting to access file " + self.workingDirectory + timeSeriesDir + "/" + hashtag + fileIdentifiers + extension)

    def read_cluster_file(self, clusterfile):
        self.clusters = {}
        inFile = open(clusterfile, 'r')
        self.dist = float(inFile.readline().strip().split(" = ")[1])
        clusterlines = inFile.readlines()
        for i in range(len(clusterlines)):
            clusterlines[i] = clusterlines[i].strip().split(",")
        clusterlines.sort(key=len, reverse=True)
        for i in range(len(clusterlines)):
            self.clusters[str(i)] = clusterlines[i]
        inFile.close()
    
    def write_salsa_json(self, timeSeriesDict, filename):
        print("writing time series json " + self.outputDirectory + "/" + filename)
        #writes individual dict time series as salsa json time series
        outFile = open(self.outputDirectory + "/" + filename + ".json", 'w')
        outFile.write("{\"date\": [")
        #needs unix epoch time or python datetime object
        dates = sorted(timeSeriesDict.keys())
        dates_string = []
        if isinstance(dates[0], datetime.datetime):
            for i in range(len(dates)):
                dates_string.append("\"" + dates[i].strftime('%s') + "\"")
        else:
            for i in range(len(dates)):
                dates_string.append( "\"" + str(dates[i]) + "\"")
        outFile.write(", ".join(dates_string))
        outFile.write("], \"" + filename + "_frequency\": [")
        values = []
        for date in dates:
            values.append(str(timeSeriesDict[date]))
        outFile.write(", ".join(values))
        outFile.write("]}")
        outFile.close()
