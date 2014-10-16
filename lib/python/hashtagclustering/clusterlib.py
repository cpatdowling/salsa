import pickle
import csv
import os
import sys
import json
from time import clock

class clustering:
    def __init__(self, dataDir="", outputDir="", clusterDist=0.835):
        if dataDir == "":
            print("no data specified when class clustering was invoked")
            sys.exit()
        self.dataDirectory = dataDir
        if outputDir == "":
            self.outputDirectory = os.getcwd() + "/default_output"
        else:    
            self.outputDirectory = outputDir
        if not os.path.exists(self.outputDirectory):
            os.mkdir(self.outputDirectory)
        self.maxDist = clusterDist
        self.progressFile = self.outputDirectory + "/cluster_log.txt"
        file = open(self.progressFile, 'w')
        file.close()

    def dist(self, correlation):
        return(1 - correlation)

    def retrieveData(self):
        #directory of files, filename without extension is taken to be hasht
        #ag, file contents are a serialized list, a json list, or an author 
        #identifier per line
        self.hashtagDict = {}
        self.dataFiles = os.listdir(self.dataDirectory)
        if self.dataFiles[0][-3:] == "csv":
            for file in self.dataFiles:
                inData = open(self.dataDirectory + "/" + file, 'r')
                authors = []
                for line in file.readlines():
                    authors = authors + [ line.rstrip(",").strip() for author in line.split(",").rstrip(",").strip() ]
                if "" in authors:
                    authors.remove("")
                self.hashtagDict[file.rstrip(".csv")] = authors
        if self.dataFiles[0][-3:] == "pck" or self.dataFiles[0][-3:] == "kle":
            for file in self.dataFiles:
                try:
                    pickleFile = open(self.dataDirectory + "/" + file, 'rb')
                    tag = file.rstrip(".pck").rstrip(".pickle")
                    self.hashtagDict[tag] = list()
                    items = pickle.load(pickleFile)
                    for item in items:
                        for author in item:
                            self.hashtagDict[tag].append(author)
                    pickleFile.close()
                except Exception as err:
                    print(file)
                    print(err)
        if self.dataFiles[0][-4:] == "json":
            for file in self.dataFiles:
                inFile = open(self.dataDirectory + "/" + file, 'rb')
                self.hashtagDict[file.rstrip(".json")] = json.loads(inFile.readlines())
        self.allAuthors = set()
        for key in self.hashtagDict.keys():
            authors = self.hashtagDict[key]
            self.allAuthors.update(authors)
        self.numAuthors = len(self.allAuthors)
        del(self.allAuthors)
        self.allHashtags = sorted(self.hashtagDict.keys())
        self.numHashtags = len(self.allHashtags)

    def appendToFile(self, fileName, s):
        fileObj = open(fileName, 'a')
        fileObj.write(s)
        fileObj.close()

    def correlate(self, x, y, numTrailZeros):
        origVecLength = len(x)
        totalVecLength = origVecLength + numTrailZeros
        xBar = float(sum(x)) / totalVecLength
        yBar = float(sum(y)) / totalVecLength
        numer = sum([ (x[i] - xBar) * (y[i] - yBar) for i in range(origVecLength) ]) + (xBar * yBar * numTrailZeros)
        denom = ((sum([ (x[i] - xBar)**2 for i in range(len(x)) ]) + (xBar**2 * numTrailZeros)) * (sum([ (y[i] - yBar)**2 for i in range(len(y)) ]) + (yBar**2 * numTrailZeros)))**0.5
        try:
            return(numer/denom)
        except ZeroDivisionError:
            return("0")

    def correlate_all(self):
        outputFile = open(self.outputDirectory + "/compiled_correlations.csv", 'w')
        cout = csv.writer(outputFile, lineterminator = '\n')
        cout.writerow([''] + self.allHashtags)
        corMatrixRow = []
        t1 = clock()
        for i in range(self.numHashtags):
            hashtag1 = self.allHashtags[i]
            hashtagData = {}
            for author in self.hashtagDict[hashtag1]:
                hashtagData[author] = [1,0]
            corMatrixRow.extend(['']*i)
            for j in range(i, self.numHashtags):
                hashtag2 = self.allHashtags[j]
                for author in self.hashtagDict[hashtag2]:
                    hashtagData[author] = hashtagData.get(author, [0]) + [1]
                corMatrixRow.append(self.correlate([ dataPoint[0] for dataPoint in hashtagData.values() ], [ dataPoint[1] for dataPoint in hashtagData.values() ], self.numAuthors - len(hashtagData)))
                t2 = clock()
                first = self.numAuthors - len(hashtagData)
                stopwatch = t2 - t1
                self.appendToFile(self.progressFile, '\t' + str(i) + ' ' + str(j) + ' ' + str(first) + ' ' + str(stopwatch) + '\n')
                t1 = clock()
                for author in hashtagData.keys():
                    if hashtagData[author][0] == 0:
                        hashtagData.pop(author)
            cout.writerow([self.allHashtags[i]] + corMatrixRow)
            corMatrixRow = []
            t2 = clock()
            self.appendToFile(self.progressFile, 'Now on hashtag ' + str(i) + ' out of ' + str(self.numHashtags) + ', which took ' + str(round((t2 - t1) / 60, 3)) + ' minutes\n')
            t1 = clock()
        outputFile.close()
        
    def correlate_single(self, hashtag1, allHashs=None):
        t1 = clock()
        if allHashs == None:
            #if not given a shared mem reference dict, use the current instance's dict, assuming one has been read into memory
            allTags = self.allHashtags
            numTags = self.numHashtags
            numAuths = self.numAuthors
            allHashs = self.hashtagDict
        else:
            numAuths = allHashs["number_of_authors"]
            allTags = sorted(allHashs.keys())
            allTags.remove("number_of_authors")
            numTags = len(allTags)
        outputFile = open(self.outputDirectory + "/" + hashtag1 + "_correlation.csv", 'w')
        cout = csv.writer(outputFile, lineterminator = '\n')
        cout.writerow([''] + allTags)
        corMatrixRow = []
        hashtag1Index = allTags.index(hashtag1)
        hashtagData = {}
        for author in allHashs[hashtag1]:
            hashtagData[author] = [1,0]
        corMatrixRow.extend([''] * hashtag1Index)
        for j in range(hashtag1Index, numTags):
            hashtag2 = allTags[j]
            for author in allHashs[hashtag2]:
                hashtagData[author] = [hashtagData.get(author, [0])[0]] + [1]
            corMatrixRow.append(self.correlate([ dataPoint[0] for dataPoint in hashtagData.values() ], [ dataPoint[1] for dataPoint in hashtagData.values() ], numAuths - len(hashtagData)))
            for author in hashtagData.keys():
                if hashtagData[author][0] == 0:
                    hashtagData.pop(author)
                else:
                    hashtagData[author] = [1,0]
        cout.writerow([hashtag1] + corMatrixRow)
        outputFile.close()
        t2 = clock()
        #Must append to master instance--multiple instances of progressFiles overwrite the original and I'll get conflicts--printing to stdout instead
        print('Now on hashtag ' + str(hashtag1Index) + " (" + hashtag1 + ') out of ' + str(numTags) + ', which took ' + str(round((t2 - t1)/ 60, 3)) + ' minutes')
        

    def compile_correlation_files(self):
        self.appendToFile(self.progressFile, 'Now compiling hashtag correlations on ' + str(self.numHashtags) + '\n')
        self.correlationMatrix = []
        for hashtag in self.allHashtags:
            inFile = open(self.outputDirectory + "/" + hashtag + "_correlation.csv", 'r')
            reader = csv.reader(inFile)
            #skipping header
            reader.next()
            index = self.allHashtags.index(hashtag)
            self.correlationMatrix.append([0] * index + reader.next()[index+1:])
            inFile.close()
        for i in range(self.numHashtags):
            self.correlationMatrix[i][i] = 1
            #symmetrizing upper triangular matrix
            for j in range(i, self.numHashtags):
                self.correlationMatrix[j][i] = self.correlationMatrix[i][j]
        outFile = open(self.outputDirectory + "/compiled_correlations.csv", 'w')
        cout = csv.writer(outFile, lineterminator = '\n')
        cout.writerow([''] + self.allHashtags)
        for i in range(self.numHashtags):
            cout.writerow([self.allHashtags[i]] + self.correlationMatrix[i])
        outFile.close()
    
    def is_in_cluster(self, hashtag):
        return(any([ hashtag in cluster for cluster in self.clusters ]))

    def immediate_cluster(self, hashtag):
        distances = self.distDict[hashtag]
        return([self.allHashtags[i] for i in range(len(self.allHashtags)) if distances[i] <= self.maxDist])

    def cluster(self):
        inFile = open(self.outputDirectory + "/compiled_correlations.csv", 'r')
        reader = csv.reader(inFile)
        reader.next()
        self.distDict = dict([ (row[0], [ self.dist(float(s)) for s in row[1:] ]) for row in reader ])
        self.clusters = []
        for hashtag in self.allHashtags:
            if self.is_in_cluster(hashtag):
                continue
            currentCluster = self.immediate_cluster(hashtag)
            checkedTags = dict([ (hashtag, False) for hashtag in currentCluster ])
            while not all(checkedTags.values()):
                currentTag = sorted([ hashtag for hashtag in checkedTags.keys() if not checkedTags[hashtag] ])[0]
                newCluster = self.immediate_cluster(currentTag)
                newTags = [ hashtag for hashtag in newCluster if not hashtag in currentCluster ]
                currentCluster += newTags
                for tag in newTags:
                    checkedTags[tag] = False
                checkedTags[currentTag] = True
            self.clusters.append(currentCluster)
        outFile = open(self.outputDirectory + "/hashtag_clusters.csv", 'w')
        cout = csv.writer(outFile, lineterminator='\n')
        cout.writerow(['maxDist = ' + str(self.maxDist)])
        for cluster in self.clusters:
            cout.writerow(sorted(cluster))
        outFile.close()
        self.appendToFile(self.progressFile, 'Clustering operation complete, ' + str(len(self.clusters)) + ' clusters found\n') 
