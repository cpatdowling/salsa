# Main.py
#
# This program

import Reader as rd
import math
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
import pandas

searchTimes = [('0' + str(i) + '0000', '0' + str(i + 1) + '0000') for i in range(9)] + [('090000','100000')] + [(str(i) + '0000', str(i+1)+ '0000') for i in range(10,24)]
Dates = [20110613,20110614,20110615,20110616,20110617,20110618,20110619,20110620,20110621,20110622,20110623,20110624,20110625,20110626,20110627,20110628,20110629,20110630,20110701,20110702,20110703,20110704,20110705,20110706,20110707,20110708,20110709,20110710,20110711,20110712,20110713,20110714,20110715,20110716,20110717,20110718,20110719,20110720,20110721,20110722,20110723,20110724,20110725,20110726,20110727,20110728,20110729,20110730,20110731,20110801,20110802,20110803,20110804,20110805,20110806,20110807,20110808,20110809,20110810,20110811,20110812,20110813,20110814,20110815,20110816,20110817,20110818,20110819,20110820,20110821,20110822,20110823,20110824,20110825,20110826,20110827,20110828,20110829,20110830,20110831,20110901,20110902,20110903,20110904,20110905,20110906,20110907,20110908,20110909,20110910,20110911,20110912,20110913,20110914,20110915,20110916,20110917,20110918,20110919,20110920,20110921,20110922,20110923,20110924,20110925,20110926,20110927,20110928,20110929,20110930,20111001,20111002,20111003,20111004,20111005,20111006,20111007,20111008,20111009,20111010,20111011,20111012,20111013,20111014,20111015,20111016,20111017,20111018,20111019,20111020,20111021,20111022,20111023,20111024,20111025,20111026,20111027,20111028,20111029,20111030,20111031,20111101,20111102,20111103,20111104,20111105,20111106,20111107,20111108,20111109,20111110,20111111,20111112,20111113,20111114,20111115,20111116,20111117,20111118,20111119,20111120,20111121,20111122,20111123,20111124,20111125,20111126,20111127,20111128,20111129,20111130,20111201,20111202,20111203,20111204,20111205,20111206,20111207,20111208,20111209,20111210,20111211,20111212,20111213,20111214,20111215,20111216,20111217,20111218,20111219,20111220,20111221,20111222,20111223,20111224,20111225,20111226,20111227,20111228,20111229,20111230,20111231,20120101,20120102,20120103,20120104,20120105,20120106,20120107,20120108,20120109,20120110,20120111,20120112,20120113,20120114,20120115,20120116,20120117,20120118,20120119,20120120,20120121,20120122,20120123,20120124,20120125,20120126,20120127,20120128,20120129,20120130,20120131,20120201,20120202,20120203,20120204,20120205,20120206,20120207,20120208,20120209,20120210,20120211,20120212,20120213,20120214,20120215,20120216,20120217,20120218,20120219,20120220,20120221,20120222,20120223,20120224,20120225,20120226,20120227,20120228,20120229,20120301,20120302,20120303,20120304,20120305,20120306,20120307,20120308,20120309,20120310,20120311,20120312,20120313,20120314,20120315,20120316,20120317]

Dates = [str(c) for c in Dates]
DateTime = []
for date in Dates:
	for time in searchTimes:
		print int(date[0:4]),int(date[4:6]),int(date[6:8])
		DateTime.append(pandas.datetime(int(date[0:4]),int(date[4:6]),int(date[6:8]),int(time[0][0:2]),0,0))

print DateTime

clusters = range(668)               #import this from files and user input
times = [12,24,48,72]
analyses = ['sd','cusum']
filters = ['gaussian','uniform']

userin1 = raw_input("Input the file location of the data: ")
data = rd.readFile(userin1)
userin2 = raw_input("Where do you want to put the new data? ")

count = 0
for t1 in times:
	for t2 in times:
		for f1 in filters:
			for f2 in filters:
				with open(userin2 + '/Cluster0011_'+f1+'_'+f2+'_'+str(t1)+'_'+str(t2)+'.csv','wb') as csvfile:
					sd = [str(DateTime[x]) for x in data[11][t1][f1][analyses[0]]] #sd list
					cu = [str(DateTime[x]) for x in data[11][t1][f1][analyses[1]]] #cusum list
					
					count += len(sd)+len(cu)
					csvwriter = csv.writer(csvfile,delimiter=',')
					csvwriter.writerow(['SD']+sd)
					csvwriter.writerow(['Cusum']+cu)
					
print count