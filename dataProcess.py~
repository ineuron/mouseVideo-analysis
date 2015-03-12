import numpy as np
import matplotlib.pylab as plt
import matplotlib.cm as colormap
import os.path
import tkFileDialog
import sys
import videoAnalysisLib as va
import dataAnalysisLib as da

#activeDir = '/lmb/home/tbranco/analysis/114491a_foraging'
activedir = sys.argv[1]
datafname = activedir+'/trackingData.txt'
avifname = activedir+'/trackingMovie.avi'
aviProps = va.getAVIinfo(avifname)

try:
  bg = np.load(activedir+'/bg.npy')
  print("Background file loaded")
except IOError:
  print("Cannot find background file ")

try:
  pmts = np.load(activedir+'/pmts.npy')
  print("Parameters file loaded")
except IOError:
  print("Cannot find parameters file ")

# Basic tracking data
print("Processing data...")
data, resultsDict, fig = va.analyseData(datafname, aviProps, bg,  pmts)
va.writeDict(resultsDict, activedir+'/trackingAnalysis.txt')
fig.savefig(activedir+'/trackingFig.pdf')

# Further analysis
pMatrix, xhist, yhist = da.getArenaMatrix(data, aviProps, plot=False)
np.save(activedir+'/arenaMatrix', [pMatrix, xhist, yhist])


