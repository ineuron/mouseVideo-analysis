# Main script to analyse movies in the cluster
# Tiago Branco - March 2014

import tkFileDialog
import numpy as np
import videoAnalysisLib as va
import subprocess
import os
import sys

mode = sys.argv[1]
totalCpus = int(sys.argv[2])
activeDir = sys.argv[3]


# Read listOfFiles.txt
try:
    with open(activeDir+'/listOfFiles.txt', 'r') as f:
        fileList = [line.strip() for line in f]
except IOError:
    print('listOfFiles.txt does not exist')

# Read times.txt
try:
    with open(activeDir+'/times.txt', 'r') as f:
        times = [line.strip() for line in f]
except IOError:
    print('times.txt does not exist')


minCpuTime = 10
#totalCpus = 100
cpus = int(totalCpus/len(fileList[1:]))
nfile = 1
print 'Using', cpus, 'cpus per file'
os.system('rm -f '+activeDir+'/file*.*')
os.system('rm -f '+activeDir+'/tracking*')

for f in fileList[1:]:
  f = fileList[0]+'/'+f
  aviProps = va.getAVIinfo(f)
  if nfile==1:
      startFrame = va.time2frame(int(times[0]), aviProps)
  else:
      startFrame = va.time2frame(0, aviProps)
  if nfile==len(fileList[1:]):
      endFrame = va.time2frame(int(times[1]), aviProps)
      if endFrame>aviProps[6]: endFrame=aviProps[6]
  else:
      endFrame = aviProps[6]
  
  if mode=='local':
      framesPerCpu = np.ceil(float(endFrame-startFrame))
      secPerCpu = va.frame2time(framesPerCpu, aviProps)
  else:
      framesPerCpu = np.ceil(float(endFrame-startFrame)/cpus)
      secPerCpu = va.frame2time(framesPerCpu, aviProps)

  #if secPerCpu < minCpuTime: 
  #    secPerCpu = minCpuTime
  #    cpus = int(np.ceil((endFrame-startFrame)/float(va.time2frame(secPerCpu, aviProps))))
      #print 'corrected cpus =', cpus
  if mode=='local':
      os.system('export SGE_TASK_ID=1')
      script = 'job.sh '+f+' '+activeDir+'/ '+str(startFrame)+' '+str(nfile)+' '+str(secPerCpu)
  else:
      #filename saveDir startFrame nfile ncall secPerCpu
      #script =  'qsub -t 1-'+str(cpus)+' -l node_type=m620+ -N job_1 -o /dev/null -e /dev/null job.sh '+f+' '+activeDir+'/ '+str(startFrame)+' '+str(nfile)+' '+str(secPerCpu)
      script =  'qsub -t 1-'+str(cpus)+' -N job_1 -o /dev/null -e /dev/null job.sh '+f+' '+activeDir+'/ '+str(startFrame)+' '+str(nfile)+' '+str(secPerCpu)
      #script =  'qsub -t 1-'+str(cpus)+' -l node_type=m620+ -N job_1 -e /dev/null job.sh '+f+' '+activeDir+'/ '+str(startFrame)+' '+str(nfile)+' '+str(secPerCpu)
  #print aviProps[6], endFrame-startFrame, va.time2frame(secPerCpu, aviProps), cpus
  #print script
  os.system(script)
  nfile+=1

script = 'sh dataMerge.sh '+activeDir+' '+str(totalCpus+1)+' '+str(len(fileList[1:]))+' '+str(cpus)
#print script
os.system(script)
