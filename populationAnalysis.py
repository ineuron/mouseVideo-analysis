import numpy as np
import matplotlib.pylab as plt
import matplotlib.cm as colormap

activeDir = '/lmb/home/tbranco/analysis/'

# Read listOfFiles.txt
try:
    with open(activeDir+'/population/listOfDirs.txt', 'r') as f:
        dirList = [line.strip() for line in f]
except IOError:
    print('listOfDirs.txt does not exist')

# Load arena background
try:
  bg = np.load(activeDir+d+'/bg.npy')
  print("Background file loaded")
except IOError:
  print("Cannot find background file ")

# Load data
data = []
for d in dirList:
    fname = activeDir + d + '/arenaMatrix.npy'
    data.append(np.load(fname))

# Separate data
matrix, xhist, yhist = [], [], []
for n in data:
    matrix.append(n[0])
    xhist.append(n[1])
    yhist.append(n[2])

# Normalize traces to total amount of time
xNorm, yNorm, matrixNorm = [], [], []
for x in xhist: xNorm.append(x/float(np.sum(x)))
for y in yhist: yNorm.append(y/float(np.sum(y)))
for m in matrix: matrixNorm.append(m/float(np.sum(m)))

# Caculate means and SEMs
xMean = np.mean(xNorm, axis=0)
xSem = np.std(xNorm, axis=0)/np.sqrt(len(xNorm))
yMean = np.mean(yNorm, axis=0)
ySem = np.std(yNorm, axis=0)/np.sqrt(len(yNorm))
matrixMean = np.mean(matrixNorm, axis=0)

# Plot data
cmapA = colormap.hot
cmapA._init()
cmapA._lut[0,3] = 0
fig = plt.figure()
ax1 = fig.add_subplot(222)
ax1.imshow(bg, cmap=colormap.gray)
ax1.imshow(matrixMean, cmap=cmapA)
ax2 = fig.add_subplot(224)
for x in xNorm:
    ax2.plot(x, 'c')
ax2.plot(xMean, 'k', lw=2)
ax3 = fig.add_subplot(221)
for y in yNorm:
    ax3.plot(y, 'c')
ax3.plot(yMean, 'k', lw=2)
plt.show()
