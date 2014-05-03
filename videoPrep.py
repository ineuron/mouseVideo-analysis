# Sets the following parameters, with user input:
#
# Background: average of N random frames
# Threshold: intensity value applied to the background subtracted image
# Diameter for morphological operations
# Boundaries for Nest and Food area, position of the nest and middle of arena
# Start and End time for analysis (start applies to 1st movie and end to last movies of the series)
#
# User selects the first file of a movie series and the script creates a $HOME/analysis/ dir with the basename
# of the file series with the following files:
#
# bg.npy - background
# pmts.npy - values for arena areas and threholding
# listOfFiles.txt - files in the series to be analysed
# times.txt - start and end time for analysis
#
# vPrep can be called with True argument to visually check the output of the parameters selected
#
# Tiago Branco - March 2014

import numpy as np
import matplotlib.pylab as plt
import os.path
import videoAnalysisLib as va
import tkFileDialog
import os
import sys

#fname = '/lmb/home/tbranco/115954a_hab2.avi'
#saveDir = '/lmb/home/tbranco/analysis/'

if len(sys.argv)>1: 
    check = sys.argv[1]
else:
    check = False

def vPrep(fname, saveDir, check=False):
  fileName = va.getFileName(fname)
  aviProps = va.getAVIinfo(fname)
  plt.ion()

  # fBackground frames
  # -----------------
  # Default values
  nFrames = 10

  bgOK = False
  bgFile = saveDir + fileName.rstrip(".avi") + "_bg.npy"
  if os.path.isfile(bgFile):
    print("Background file exists, loading...")
    bg = np.load(bgFile)
  else:
    print("Generating background with default settings...")
    bg  = va.getBg(fname, aviProps, nFrames)
  if check:
    while not bgOK:
      plt.figure()
      plt.imshow(bg)
      plt.set_cmap('gray')
      plt.show()
      uDecision = raw_input("Background OK? [y]es; [n]o ")
      if uDecision=='y': 
          bgOK = True
      else:
          uframes = raw_input("Select number of frames ")
          bg  = va.getBg(fname, aviProps, int(uframes))
  np.save(saveDir + 'bg', bg)
  print('Background file saved')

  # Threshold
  # --------------
  # Default values
  ths = 15
  morphDiameter = 5

  pmtsFileExists = False
  thsOK = False
  pmtsFile = saveDir + fileName.rstrip(".avi") + "_pmts.npy"
  if os.path.isfile(pmtsFile):
    print("Parameters file exists, loading...")
    pmtsFileExists = True
    filePmts = np.load(pmtsFile)
    ths, morphDiameter = va.setThreshold(fname, aviProps, bg, filePmts[0][0], filePmts[1][0])
  else:
    print("Generating threshold with default settings...")
    ths, morphDiameter = va.setThreshold(fname, aviProps, bg, ths, morphDiameter)
  if check:
    while not thsOK:
      uDecision = raw_input("Threshold OK? [y]es; [n]o ")
      if uDecision=='y': 
          thsOK = True
      else:
          while True:
              try:
                  uths = int(raw_input("Select new threshold "))
                  umorph = int(raw_input("Select new diameter to erode and dilate "))
                  break
              except ValueError:
                  print("Invalid number, please try again ")
          ths, morphDiameter = va.setThreshold(fname, aviProps, bg, uths, umorph)

  # Arena areas
  # --------------
  # Default values
  nestPos = [145, 600]
  nestArea = [(32,690),(220,680),(210,520)]
  arenaCenter = [570,605]
  foodArea = [(795,735),(935,735),(940,605)]

  plt.ioff()
  arenaOk = False
  if pmtsFileExists:
    print("Using parameters file...")
    va.plotArena(aviProps, filePmts, bg)
    pmts = [[ths], [morphDiameter], filePmts[2], filePmts[3], filePmts[4], filePmts[5]]
  else:
    print("Generating arena with defauls settings...")
    pmts = [[ths], [morphDiameter], nestPos, nestArea, arenaCenter, foodArea]
    va.plotArena(aviProps, pmts, bg)
  if check:
    while not arenaOk:
      uDecision = raw_input("Arena OK? [y]es; [n]o ")
      if uDecision=='y':
          arenaOk = True
      else:
          print("Select new arena ")
          points = va.setPoints(fname, aviProps, bg)
          pmts = [[ths], [morphDiameter], points[0], points[1], points[2], points[3]]

  #print pmts[0], pmts[1]
  #fsaveName = saveDir + fileName.rstrip(".avi") + "_pmts"
  np.save(saveDir + 'pmts', pmts)
  print('Parameters file saved')


# --------------------------------------------------------------------------------------
# Select movies to analyse
initialdir = '/lmb/home/tbranco/data'
#initialdir = '/lmb/home/tbranco/testdata'
fname = tkFileDialog.askopenfilenames(title='Choose the 1st file of the movie series', initialdir=initialdir, filetypes=[('Movie files', '*.avi')])

directory, filename = os.path.split(fname[0])
basename = filename.rstrip('.avi')
adir = '/lmb/home/tbranco/analysis/' + basename + '/'
os.system('mkdir -p '+ adir)

while True:
  try:
    tStart = int(raw_input("Select start time "))
    tEnd = int(raw_input("Select end time "))
    break
  except ValueError:
    print("Invalid number, please try again ") 

temp = sys.stdout
sys.stdout = open(adir+'listOfFiles.txt', 'w')
print directory
filenames = []
for f in os.listdir(directory):
    if f.startswith(basename):
        #n = len(f.rstrip('.avi'))-len(basename)+1
        #os.system('ln -s '+directory+'/'+f+' '+tempdir+'/file.'+str(n))
        filenames.append(f)

# Order filenames and print to file
counter = 0
while counter<len(filenames):
    n = -1
    nfile = 0
    while n!=counter:
        f = filenames[nfile]
        n = len(f.rstrip('.avi'))-len(basename)    
        nfile+=1
    print f 
    counter+=1

sys.stdout.close()
sys.stdout = open(adir+'times.txt', 'w')
print tStart
print tEnd
sys.stdout = temp

# Define parameters
vPrep(fname[0], adir, check=check)

