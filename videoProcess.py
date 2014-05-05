
import numpy as np
import matplotlib.pylab as plt
import os.path
import sys
import subprocess
import videoAnalysisLib as va

#fname = '/lmb/home/tbranco/115954a_hab2.avi'
#saveDir = '/lmb/home/tbranco/analysis/'

# Input arguments:
# filename saveDir startFrame nfile secPerCpu
# Note: filename has full path

fname = sys.argv[1]
saveDir = sys.argv[2]
#fname = subprocess.check_output('readlink '+fname, shell=True)
#fname = fname.rstrip('\n')
startFrame = int(sys.argv[3])
#tEnd = int(sys.argv[4])
nfile = sys.argv[4]
ncall = sys.argv[5]
if len(ncall)==1: ncall='0'+ncall
secPerCpu = float(sys.argv[6])

nestThreshold = 10
aviProps = va.getAVIinfo(fname)
print fname, aviProps
fileName = va.getFileName(fname)
trackFname = saveDir + 'file' + str(nfile) + '_' + ncall + '.txt'
aviFname = saveDir + 'file' + str(nfile) + '_' + ncall + '.avi'
bgSubFname = saveDir + 'file' + str(nfile) + '_' + ncall

tStart = va.frame2time(startFrame, aviProps) + (int(ncall)-1)*secPerCpu
tEnd = tStart + secPerCpu
print tStart, tEnd
while True:
  try:
      print(saveDir+"bg.npy")
      bg = np.load(saveDir + "bg.npy")
      print("Background file loaded")
  except IOError:
      print("Cannot find background file ")
      break

  try:
      pmts = np.load(saveDir + "pmts.npy")
      print("Parameters file loaded")
  except IOError:
      print("Cannot find parameters file ")
      break

  print("Processing video...")
  mousePositions, meanFrame = va.processFrames(fname, aviFname, aviProps, tStart, tEnd, bg, pmts, nestThreshold, saveAVI=True)
  np.savetxt(trackFname, mousePositions)
  np.save(bgSubFname, meanFrame)
  #data, results = va.analyseData(trackFname, aviProps, bg,  pmts, PLOT=False)
  #print(".AVI output file saved")
  break
