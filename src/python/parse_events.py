#Chase Dowling, chase.dowling@pnnl.gov, August 2014

import sys
import pathConfig

from eventcomparison import extractEvents


inData = sys.argv[1]
outDir = sys.argv[2]
try:
    size = int(sys.argv[3])
except:
    size = 8

parser = extractEvents.events(inData, outDir, size)
parser.parse_cusum_output()
