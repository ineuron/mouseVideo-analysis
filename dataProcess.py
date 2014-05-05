import numpy as np
import matplotlib.pylab as plt
import matplotlib.cm as colormap
import os.path
import tkFileDialog
import sys
import videoAnalysisLib as va

# Auxiliary functions
def getArenaMatrix(data, aviProps, plot=True):
    xData = data[:,0:1]
    yData = data[:,1:2]
    binSize = 10.0
    ylim = bg.shape[1]
    xlim = bg.shape[0]
    pMatrix = np.zeros([xlim, ylim])
    histMatrix = np.zeros([xlim/binSize, ylim/binSize])

    # Make matrices
    xcounter = 0
    for x in np.arange(0, xlim, binSize):
       ycounter = 0
       for y in np.arange(0, ylim, binSize):
           pMatrix[x:(x+binSize), y:(y+binSize)] = np.sum(((xData>x) & (xData<(x+binSize))) & ((yData>y) & (yData<(y+binSize))))
           histMatrix[xcounter, ycounter] = np.sum(((xData>x) & (xData<(x+binSize))) & ((yData>y) & (yData<(y+binSize))))
           ycounter+=1
       xcounter+=1

    timePerFrame = 1./aviProps[4]
    yaxis = histMatrix.sum(axis=1) * timePerFrame
    xaxis = histMatrix.sum(axis=0) * timePerFrame

    # Plot
    if plot:
      cmapA = colormap.hot
      cmapA._init()
      cmapA._lut[0,3] = 0
      fig = plt.figure()
      ax1 = fig.add_subplot(222)
      ax1.imshow(bg, cmap=colormap.gray)
      ax1.imshow(pMatrix, cmap=cmapA)
      ax2 = fig.add_subplot(224)
      ax2.plot(xaxis)
      ax3 = fig.add_subplot(221)
      ax3.plot(yaxis)
      plt.show()
    return pMatrix, xaxis, yaxis

# -------------------------------------------------------------------------------
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

# Basic tracking data
print("Processing data...")
data, results, fig = va.analyseData(datafname, aviProps, bg,  pmts)
va.writeDict(results, activedir+'/trackingAnalysis.txt')
fig.savefig(activedir+'/trackingFig.pdf')

# Further analysis
pMatrix, xhist, yhist = getArenaMatrix(data, aviProps)
np.save(activedir+'/arenaMatrix', [pMatrix, xhist, yhist])



