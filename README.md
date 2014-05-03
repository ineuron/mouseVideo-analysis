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
Currently the video data acquired from a single experiment 

1. Run videoPrep 
2.
