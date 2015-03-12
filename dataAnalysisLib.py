import numpy as np
import matplotlib.pylab as plt
import matplotlib.cm as colormap
import os.path
import sys
import videoAnalysisLib as va


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

def getNumbers(s):  # get numbers from trackingAnalysis.txt
    out = []
    for t in s.split():
        n = ''.join(ele for ele in t if ele.isdigit() or ele == '.')
        if len(n)>0: out.append(float(n))
    return out

def nestRunPlotVertical(runsStart, runsDur, ax):
    nestTimeCounter = 0
    nestX = [0,0]
    for r in np.arange(0, len(runsDur)):
        if (r == len(runsDur)-1):              # last run exception
            nestTime = totalDur-(runsStart[r]+runsDur[r])
        elif (r==0) & (runsStart[0]<>0):       # fist run exception
            nestTime = runsStart[r]
        else:
            nestTime = runsStart[r+1]-(runsStart[r]+runsDur[r])
        nestY = [nestTimeCounter, nestTimeCounter + nestTime]
        runX = [0, runsDur[r]]
        if runsStart[0]==0:    
            runY = [nestTimeCounter, nestTimeCounter]
        else:
            runY = [nestTimeCounter+nestTime, nestTimeCounter+nestTime]
        nestTimeCounter = nestTimeCounter + nestTime
        ax.plot(runX,runY, 'g', lw=2)
        ax.plot(nestX,nestY, 'r', lw=2, marker='o', markerfacecolor='w', markeredgecolor='w')
    ax.set_xlim([-20, nestTimeCounter+20])
    ax.set_ylim([-20, nestTimeCounter+20])

def getLoomOnsets(trackData, aviProps):
   loomOnsets = []
   n = 0
   timePerFrame = 1./aviProps[4]
   while n<len(trackData):
       if trackData[n,2]>4000000:
           loomOnsets.append(n*timePerFrame)
           n = n + 250
       else:
           n+=1
   return loomOnsets

def nestRunPlot(data, trackData, aviProps):  # 'data' is from trackingAnalysis.txt
  runsDur = getNumbers(data[0])
  runsStart = getNumbers(data[4])
  totalTime = getNumbers(data[2])[0] + getNumbers(data[8])[0]
  fig = plt.figure()
  ax1 = fig.add_subplot(211)
  ax2 = fig.add_subplot(212) 
  if runsStart[0]==0: # Remove 1st run data if movie starts with mouse running
      del runsDur[0]
      del runsStart[0]
  nestTimes, runTimes = [], []             # Get nest times
  for r in np.arange(0, len(runsDur)):
      if (r==0):                           # first run exception
          tNest = runsStart[r]
      else:
          tNest = runsStart[r]-(runsStart[r-1]+runsDur[r-1])
      tRun = runsDur[r]
      nestTimes.append(tNest)
      runTimes.append(tRun)
  # Tidy up times
  # If time in area is too small don't count as event and add it to next if it's a short run (it stayed in the nest)
  # or add it to the previous if the nest time is short (it continued running)
  # The difference is because the nest time is the time in nest before the run in the same line, so there is a temporal order
  # For now the 1st and last datapoints are ignored
  areaTimes = np.zeros([len(nestTimes), 2])
  areaTimes[:,0] = np.array(nestTimes)
  areaTimes[:,1] = np.array(runTimes)
  timeCutOff = 0.5          
  oAreaTimes = areaTimes.copy()
  pos = np.array([0,1])
  for t in np.arange(1, len(areaTimes)-1):
    test = areaTimes[t]<timeCutOff
    if np.sum(test)==1:
        if pos[test]==1:
            areaTimes[t+1] = areaTimes[t+1] + areaTimes[t]
            areaTimes[t] = [0,0]
        if pos[test]==0:
            n=1
            while np.sum(areaTimes[t-n])==0:        # in case we have made the previous line [0,0]
                n+=1
            areaTimes[t-n] = areaTimes[t-n] + areaTimes[t]
            areaTimes[t] = [0,0]
    if np.sum(test)==2:
        areaTimes[t] = [0,0]
  areaTimes = areaTimes[(areaTimes>1)[:,0]]
  # Get Loom times and positions
  loomOnsets = getLoomOnsets(trackData, aviProps)
  plotTimes = np.sum(areaTimes, axis=1)
  for n in np.arange(0, len(plotTimes)):
    if n==0:
        plotTimes[n] = plotTimes[n]
    else:
        plotTimes[n] = plotTimes[n] + plotTimes[n-1]
  loomPos = []
  for l in loomOnsets:
    loomPos.append(np.argmin(np.abs(plotTimes-l)))
  # Plot Nest and Runs times
  offset = 1
  yOffset = 10  
  for n in np.arange(0, len(areaTimes)):
    ax1.plot([offset,areaTimes[n,1]+offset],[n,n], 'y', lw=2)        # Run 
    ax1.plot([-offset,-(areaTimes[n,0]+offset)],[n,n], 'r', lw=2)    # Nest
    if n in loomPos: ax1.plot(areaTimes[n,1]+offset, n, marker='o', markerfacecolor='k', markeredgecolor='k') 
  ax1.set_xlim([-100, 100])
  ax1.set_ylim([-yOffset,len(areaTimes)+yOffset])
  # Distributions
  ax2.hist(-areaTimes[:,0], range=(-100,0), color='r', histtype='stepfilled')
  ax2.hist(areaTimes[:,1], range=(0,100), color='y', histtype='stepfilled')
  ax2.set_xlim(ax1.get_xlim())
  plt.show()







