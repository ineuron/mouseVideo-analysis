# Read numpy arrays and merge them into a single one

import sys
import numpy as np
import matplotlib.pylab as plt

DIR = sys.argv[1]
nfiles = sys.argv[2]
njobs = sys.argv[3]

frames = []
print 'Concatenating numpy frames...'
for f in np.arange(1, int(nfiles)+1):
    for j in np.arange(1, int(njobs)+1):
        if j<10:
            fname = DIR+'/file'+str(f)+'_0'+str(j)+'.npy'
        else:
            fname = DIR+'/file'+str(f)+'_'+str(j)+'.npy'
        frame = np.load(fname)
        frames.append(frame)
        print fname

mFrame = np.mean(frames, axis=0)
mFrame[mFrame<0] = 0

fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(mFrame)
fig.savefig(DIR+'/trackingMeanFrame.pdf')
np.save(DIR+'/trackingMeanFrame', mFrame)
