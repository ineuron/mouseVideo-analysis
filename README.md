mouseVideo-analysis
===================

Analysis of videos of single mice wondering about in a behavioural arena. Does some very basic tracking and spits out the center of mass for each frame, plus a buch of minor computations, like time spent in defined areas, distance travelled, speed, etc. Saves .avi file with binary mask on top of original video.

Requirements:
-------------
Python with standard libraries and OpenCV with FFMEG

Only tested properly in Linux. Early versions worked on Windows and MacOS X, but the code would probably require some tweaking to work now.


List of files:
--------------
videoAnalysisLib.py - library of functions to perform tracking, analysis, file I/O, everything really
videoPrep.py - routines to define background, threshold, arena areas and segement of movie sequence to analyse
VideoProcess.py - 
VideoAnalysisMain.py - 


Workflow:
---------
Currently the video data acquired from a single experiment is saved across multiple .avi files, which are processed as a movie series.

1. python videoPrep.py [True] - select the movie series and the various parameters required to process the movie files. The "True" argument is optional is if present allows visual inspection of the outcome of the selected paramters. A analysis folder is automatically created with the basename of the series where all analysis data will be saved.
2.
