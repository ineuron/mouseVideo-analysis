import numpy as np
import matplotlib.pylab as plt
import os.path
import tkFileDialog
import sys
import videoAnalysisLib as va

#activedir = '/lmb/home/tbranco/analysis/testmovie'
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

print("Processing data...")
data, results, fig = va.analyseData(datafname, aviProps, bg,  pmts)

va.writeDict(results, activedir+'/trackingAnalysis.txt')
fig.savefig(activedir+'/trackingFig.pdf')
