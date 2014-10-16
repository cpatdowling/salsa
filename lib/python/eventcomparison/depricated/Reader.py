import os

#all the options of analyesis types
analyses = ['cusum','sd']
filters = ['gaussian','uniform']
times = [12,24,48,72]

#create output structure
def initOutput(clusterlen=668):
	out = []
	for x in range(clusterlen):
		tout = {}
		for t in times:
			fout = {}
			for f in filters:
				aout = {}
				for a in analyses:
					aout[a]=[]
				fout[f]=aout
			tout[t]=fout
		out.append(tout)
		
	return out
		
def eventList(clusterFile):
	lines = []
	out = []
	with open(clusterFile) as f:
		lines = f.readlines()
	for s in lines:
		if s[:19]=='Event Centered at: ':
			out.append(int(s[19:len(s)-1]))
	return out
		
	
def readFile(location = './data'):
	listdir = os.listdir(location)
	listdir.reverse()
	
	listdir.remove('hourly_events')

	out = initOutput()
	for a in analyses:
		for f in filters:
			for t in times:
				filedir = location + '/' + listdir.pop()
				clist = os.listdir(filedir)
				firstitem = int(clist[0][7:11])
				for c in range(firstitem,len(clist)):
					out[c][t][f][a] = eventList(filedir + '/' + clist[c])
					
	return out
	
def convertToMatlab(data):
	clusters = range(668)
	for c in clusters:
		for t in times:
			for f in filters:
				with open('./MatLabData/'+f+'/'+str(t)+'/'+'cluster'+ ('%05d' % c)+'_events.csv', 'w+') as csvfile:
					csvwriter = csv.writer(csvfile, delimeter = ',')
					csvwriter.writerow(analyses[0],data[c][t][f][analyses[0]])
					csvwriter.writerow(analyses[1],data[c][t][f][analyses[1]])