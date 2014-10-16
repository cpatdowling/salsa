#Chase Dowling, chase.dowling@pnnl.gov, Aug 2014
#This script aggregates the output of the managed hashtag clustering
#script

import sys
import pathConfig

from hashtagclustering import aggregatelib

#number of topk clusters to output
numClusters = sys.argv[1]

clusteringOutputDir = sys.argv[2]
originalDataDir = sys.argv[3]

aggregation = aggregatelib.aggregate(outputDir=sys.argv[4])

clusters = aggregation.read_cluster_file(clusteringOutputDir + "/hashtag_clusters.csv")

print("aggregating time series")
aggregation.retrieve_series_data(originalDataDir, fileIdentifiers=".ts", extension="pickle")

clusterRef = open(aggregation.outputDirectory + "/cluster_reference.txt", 'w')
clusterRef.write("cluster distance: " + str(aggregation.dist) + "\n")
for i in range(int(numClusters)):
    name = "cluster_" + str(i+1)
    aggregation.write_salsa_json(aggregation.timeSeries[str(i+1)], name)
    clusterRef.write("cluster " + str(i) + ": " + ",".join(aggregation.clusters[str(i)]) + "\n")

clusterRef.close()
