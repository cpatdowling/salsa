#Chase Dowling, 09/16/2013, chase.dowling@pnnl.gov

version 0.1.0

SALSA is currently in beta. Things will break, particularly when using versions of R greater than 3.0.1

SALSA is designed for the analysis of large amounts of web social media data
--time series and graphical data--by collecting and counting features within
 the data, detecting and clustering events in the feature data, and predicting event types in time series.

===System Requirements===

    -Python 2.7.3 or greater
    -Matlab 2012a or greater
    -R-3.0.1 or (R is being transitioned to Numpy due to deep R-3.1.1 compatability issues)
    -UNIX based OS (Limited/untested Windows compatability)

===Included Analytics===

    -a parallel implementation of the hashtag clustering topic
modeler in "SociAL Sensor Analytics: Measuring Phenomenology At Scale" (http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=6578787&tag=1)

    -an implementation of Periodic Generalized Cumulative Sum for time series
     event detection

    -an implementation of Yang's K-Spectral Centroid clustering algorithm for
     time series event clustering (http://dl.acm.org/citation.cfm?id=1935863)

    -an implementation of mutliple-time series feature SVM classification of
     detected events


===Installation===

1. From the root ~/salsa directory call: python makeAll.py
2. You're done.


2. Launch R from ~/salsa/src/R -- confirmation message/info will display:
	"Running salsaOnR..."
3. All appropriate depedencies will be loaded for an interactive session
and command line calls from appropriate ~/salsa/src directories.
3.5  All neccessary R packages are preinstalled and compiled in /salsa/src/R/-
    packages or windows_packages depending on working environment
4. From command line: >>Rscript salsaBatchMode.R -i /salsa/test/testJSONTS.json
	You'll find the output in the /salsa root directory.*
	
*Starred items are to be problems phased out to simplify installation process.

===Workflow===

Overview:

Designed for abberation detection in heteroscedastic/non-stationary time serie-
s prototypical of web data.  Includes basic descriptive statistics, Fourier an-
alysis, statistical event detection and extraction, and event type prediction.

One or multiple time series are passed to a stateless analytics platform along 
with specified analyses, and each time series is returned in an equivalent JSON
format along with the output of those required analyses.

Hashtag Clustering Topic Modeling:
    Input Requirements:
        -JSON, python serialized/pickle, or csv file
    Output:
        -Hashtag clusters based on author usage

I/O object Descript:

Input:
    

Fourier & Time Series Analysis/Event Detection:
	Input Requirements:
		-JSON time series object**
	Optional Input:
		-JSON formatted list of analyses to be performed
		or a string of capital letters inidicating which
		analyses are desired.
		-JSON formatted list of custom parameters
		-Filepath for output
	Output:
		-JSON formatted time series w/ analyses
		
	Example Objects:
		Input: ~/salsa/test/testJSONTS.json
		Custom Parameters: ~/salsa/test/testJSONPARAM.json
		Analyses: ~/salsa/test/testANALYSES.json
		
	**(all inputs may be URLs or filepaths)

I/O object Description:

Input:
	Data: A series of time dependent values in JSON dictionary/hashmap for-
	mat.  Prefered string date format: 'yyyyMMDDhhmmss'.  Key value is 
	'date' for time series column names, value is an array for values for a
	specific date.
	
		Dates, column names, and 'date' first key value are all strings  
		Time series values are integers.  Date values must be strings 
		because R is natively 32-bit and integer dates will overflow.
	
		{
		'date':['series1', 'series2'],
		'yyyyMMDDhhmmss':[series1value1, series2value1],
		'yyyyMMDDhhmmss':[series1value2, series2value2],
		'yyyyMMDDhhmmss':[series1value3, series2value3]
		}
	
	Parameters:  A key value JSON dictionary/hashmap specifying which para-
	meters need to be updated and their specified value.
	
		{
		'parameterName': value,
		'parameterName2': value,
		}
		
	Defaults:
	
		{
		"filter":"uniform",
		"threshold":10,
		"window":100,
		"reference":0,
        "control":1,
		"resetVal":0,
		"falseAlarm":0.05,
        "fftThreshold":2,
        "fftDampenFactor":.8
		}
		
		Defaults are loaded in a minimal R instance with each instance.
		They're not stored as a JSON object--if an error is encountered
		reading custom parameters from JSON, the salsaOnR instance will
		revert to default parameters.  See R init details below.
		
	Paramter names, acceptable values, and descriptions:
		
		"filter" : "uniform", "gaussian", "exponential", "linear"
		
			Type of filter used when smoothing data, for example, a
			moving average is a uniform filter.  Parameter value 
			must be string
		
		"threshold": a float value greater than 1
		
			Log-likelihood value before GenCusum throws an event 
			alert
			
		"window": an even integer value, typically 0 mod 12
		
			Width of filter--must be an even integer.
		
		"falseAlarm": decimal value between 0 and 1
		
			Percentage of acceptable false alarms detected by the 
			GenCusum algorithm
			
		"resetVal": integer value between 0 and threshold value
		
			When an event is detected, what Cusum score should be
			reset to?  Typically fixed at 0, not tested for other
			values in non-stationary time series.
			
			Note: Setting to threshold value may return time depend
			ent event detection i.e. when event begins/ends.

        "fftThreshold": a float value greater than 1

            When using the band reject filter on time series data to 
            remove periodic behavior, this value determines the sensitivity
            to detected periods.  This value is exactly the number of standard
            deviations of the mean of the FFT transform of the data to accept.

        "fftDampenFactor": a non-zero float value between 0 and 1

            For rejected bands, this value determines the amount by which to
            dampen them.
			
	Analyses:  What analyses should be performed on input data?  If multipl
	analyses are specified along with custom parameters, all analyses are 
	performed with those custom parameters on specified data in the current
	instance.  
		
		Default analyses are an undamped generalized cumulative sum and
		and heuristic event detection.
		
	Analyses JSON object or command line string:
		
	Examples:	
		JSON object: ["U", "F"]
        
  	Command line: >>Rscript salsaBatchMode -i /path/to/data -a UF
		
	Analyses types:
		"G": damped generalized cumulative sum
		"U": undamped generalized cumulative sum
		"M": outlier filter
		"F": heuristic event detection
		
		Details on each of these analyses can be found in the 
		~salsa/lib/R section below.

Output:
	Data: For each time series passed in, a JSON object will be written for
	each to the specified filepath or the working directory ~/salsa of the 
	same format as the original data.  
	
	Example output:
	{
	'date',['series1','filter','standev','eventNum'],
	'yyyyMMDDhhmmss':[series1value1,filterval,standeval,0]
	'yyyyMMDDhhmmss':[series1value2,filterval,standeval,0]
	'yyyyMMDDhhmmss':[series1value3,filterval,standeval,0]
	'yyyyMMDDhhmmss':[series1value4,filterval,standeval,1]
	'yyyyMMDDhhmmss':[series1value4,filterval,standeval,1]
	'yyyyMMDDhhmmss':[series1value4,filterval,standeval,1]
	'yyyyMMDDhhmmss':[series1value4,filterval,standeval,1]
	'yyyyMMDDhhmmss':[series1value4,filterval,standeval,2]
	'yyyyMMDDhhmmss':[series1value4,filterval,standeval,2]
	'yyyyMMDDhhmmss':[series1value4,filterval,standeval,2]
	'yyyyMMDDhhmmss':[series1value4,filterval,standeval,2]
	}
	
	The final value, 'eventNum' is a counter that goes up when the alert
	'switch' is thrown.  The first occurence of 1 is the time stamp for
	when an event was detected.
	
==Init Details==

==Library Descriptions==

    python
        hashtagclustering
            module clusterlib
                class clustering
                -This class initializes a clustering instance

                    function __init__(self, dataDir="", outputDir="", clusterDist=0.835)	
		            -When initializing a clustering instance, specify the directory 
                     containing the data, the desired output directory (creates a default
                     in the current working directory if non specified) and the cluster
                     distance (from 0 to 1, inclusive)

                    function retrieveData(self)
                    -reads data from the instance input data directory. File names are
                     presumed to be hashtags, CSV files contain lists of comma separated
                     authors by line or over multiple lines, serialized files contain
                     lists of authors.

                    function correlate(self, x, y, numTrailZeros)
                    -calculates the correlations of two binary vectors where each element
                     of the vector is a boolean variable indicating for a given hashtag
                     whether or not an author used it

                    function correlate_all(self)
                    -attempts to correlate all hashtags by author usage in a single 
                     clustering instance

                    function correlate_single(self, hashtag1)
                    -correlates hashtag1 with all other hashtags currently held in the 
                     clustering instance's memory

                    function compile_correlation_files(self)
                    -compiles the outputs of correlate_single to relect the symmetric
                     matrix output of correlate_all

                    function immediate_cluster(self, hashtag)
                    -finds all hashtags within the correlative distance for the given
                     clustering instance for a given hashtag

                    function cluster(self)
                    -performs the clustering operation on a correlation matrix of all 
                     hashtags to one another
    
    R
		
		
		
		




