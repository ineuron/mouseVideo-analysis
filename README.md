mouseVideo-analysis
===================

Analysis of videos of single mice wondering about in a behavioural arena. Does some very basic tracking and spits out the center of mass for each frame, plus a buch of minor computations, like time spent in defined areas, distance travelled, speed, etc. Saves .avi file with binary mask on top of original video.

Requirements:
-------------
Python with standard libraries and OpenCV with FFMPEG. Transcode for running avimerge.

Only tested properly in Linux. Early versions worked on Windows and MacOS X, but the code would probably require some tweaking to work now.


List of files:
--------------
videoAnalysisLib.py - library of functions to perform tracking, analysis, file I/O, everything really

videoPrep.py - routines to define background, threshold, arena areas and segement of movie sequence to analyse

videoProcess.py - runs tracking algorithm

main.py - coordinates and starts videoProcess, dealing with the cluster when in cluster mode

dataProcess.py - runs analysis routines

dataMerge.sh - merges .multiple avi files into one

job.sh - used for submiting videoProcess to the cluster



Workflow:
---------
Currently the video data acquired from a single experiment is saved across multiple .avi files, which are processed as a movie series. Analysis can be done in the local computer or submitted to Gridengine for processing in the MRC LMB cluster. Some paths are hardcoded and assume that code is in $HOME/code/github/mouseVideo-analysis.

1. python videoPrep.py [False] - select the movie series and the various parameters required to process the movie files. The "False" argument is optional is if present ommits visual inspection of the outcome of the selected parameters. A analysis folder is automatically created with the basename of the series where all analysis data will be saved.

2. python main.py MODE CPUS ACTIVE_DIR - MODE is "local" or "cluster", CPUS is the number of cpus to use in cluster mode and ACTIVE_DIR is the analysis folder generated by videoPrep. The script calls job.sh which starts videoProcess.py, and then dataMerge.sh for producing the final tracking movie and data files. dataMerge.sh also runs dataProcess.py which analyses the tracking data, saves .txt file with data and .pdf file with tracking runs. 

Note - dataMerge.sh has to be run locally as avimerge doesn't exist in the LMB cluster.



