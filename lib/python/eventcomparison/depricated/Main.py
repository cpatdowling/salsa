# Main.py
#
# This program

import Reader as rd
import math
import numpy as np
import matplotlib.pyplot as plt
import os

clusters = range(668)               #import this from files and user input
times = [12,24,48,72]
analyses = ['sd','cusum']
filters = ['gaussian','uniform']

userin = raw_input("Input the file location of the data: ")
data = rd.readFile(userin)

def getOutput(threshold):
	print 'Getting Output'
	output = rd.initOutput(len(clusters))
	wait = ''
	for c in clusters:
		for t in times:
			for f in filters:
				dic = data[c][t][f]
				sd = dic[analyses[0]] #sd list
				cu = dic[analyses[1]] #cusum list

				total_matchingsd = 0
				total_matchingcu = 0

				#now that everything is loaded, we are going to run through each item in sd, and compare see if it matches an item in cusum within one hour. If true, add 1 to total_matching.
				for n in sd:
					for r in cu:
						if math.fabs(n-r)<=threshold:
							total_matchingsd += 1
							break
			
				#now that everything is loaded, we are going to run through each item in sd, and compare see if it matches an item in cusum within one hour. If true, add 1 to total_matching.
				for n in cu:
					for r in sd:
						if math.fabs(n-r)<=threshold:
							total_matchingcu += 1
							break

				if len(cu) != 0: matching_vs_cu = float(total_matchingcu)/float(len(cu))*100
				else: matching_vs_cu = 'NA'
	
				if len(sd) != 0: matching_vs_sd = float(total_matchingsd)/float(len(sd))*100
				else: matching_vs_sd = 'NA'
	
				output[c][t][f][analyses[0]]=matching_vs_sd
				output[c][t][f][analyses[1]]=matching_vs_cu
			
				#Debugging Purposes
				#print sd
				#print cu
				#print (total_matchingsd,total_matchingcu)
				#print (matching_vs_sd,matching_vs_cu)
				#wait = raw_input("PRESS ENTER TO CONTINUE. ")
				#if wait == 'q':
				#	break
			#if wait == 'q':
			#	break
		#if wait == 'q':
		#	break
			
	return output
	
def plotData(output,clusters,filter1,filter2,time1,time2,pltsize,name='0'):
	print 'Printing: ' + name
	sddata = []
	cudata = []
	for x in clusters:
		cudata.append(output[x][time1][filter1]['cusum'])
		sddata.append(output[x][time2][filter2]['sd'])
	
	counter = 0
	
	numgraphs = int(math.ceil(len(clusters)/pltsize))
	clusters.sort()
	clusters.reverse()
	
	if name != '0': os.mkdir('./save/'+name)
	
	for n in range(numgraphs+1):
		templist, tempcu, tempsd = [], [], []
		if len(clusters)<pltsize:
			pltsize = len(clusters)
		for i in range(pltsize):
			c = clusters.pop()
			templist.append(c)
			if cudata[c]=='NA': cudata[c]=0
			if sddata[c]=='NA': sddata[c]=0
			tempcu.append(cudata[c])
			tempsd.append(sddata[c])

		plt.figure(n)
		cuplot = plt.bar(np.array(templist),tempcu,width=0.35,color='r')
		sdplot = plt.bar(np.array(templist)+0.35,tempsd,width=0.35,color='y')
		temparray = np.array(templist)
		plt.xticks(temparray+0.35, temparray)
		plt.xlim([np.min(temparray)-.35,np.max(temparray)+.35*3])
		plt.ylim([0,100])
		plt.legend([cuplot,sdplot],['Cusum','SD'])
		if name != '0':
			plt.savefig('./save/'+name+'/graph'+str(n)+'.png')
			plt.close()
		else: show()

	
output = getOutput(1)
#t1, t2, f1, f2 = 72, 72, 'gaussian', 'uniform'
#plotData(output,range(668),f1,f2,t1,t2,10,'All_'+f1+'_'+f2+'_'+str(t1)+'_'+str(t2))

for t1 in times:
	for t2 in times:
		for f1 in filters:
			for f2 in filters:
				try:
					plotData(output,range(668),f1,f2,t1,t2,10,'All_'+f1+'_'+f2+'_'+str(t1)+'_'+str(t2))
				except WindowsError as inst:
					break
		

#"""
#try:
#	stuff for things
#except Exception as inst:
#	print inst
#	print inst.args
#	print Exception
#	
#try:
#	stuff for things
#except:
#	continue
#"""
