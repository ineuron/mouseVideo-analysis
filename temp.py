import numpy as np
from scipy.stats import ks_2samp
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
import videoAnalysisLib as va
import dataAnalysisLib as da
import smooth as smooth


dirList = []
#dirList.append('/fhgfs/brancolab/1697_ON_top/')
#dirList.append('/lmb/home/tbranco/analysis/1694_ON_top')
dirList.append('/lmb/home/tbranco/analysis/97936_top_complete')
#dirList.append('/lmb/home/tbranco/analysis/95757_top/')
#dirList.append('/lmb/home/tbranco/analysis/114491e_foraging/')

def plotTrackingData(trackingData, props):
    colors = ['Crimson', 'CornflowerBlue', 'DarkOliveGreen', 'DarkOrange', 'LightSlateGray']
    nData = len(trackingData) 
    # Prepare plots
    fig = plt.figure(figsize=(20, 4*nData))
    gs = gridspec.GridSpec(nData,3, width_ratios=[1,6,1])
    ax, dataOut = [], []
    for d in np.arange(0, len(trackingData)):
        aviProps = props[d]
        trackData = trackingData[d]
        dataOut.append(trackData[:,1])
        ax1, ax2, ax3 = d*3+0, d*3+1, d*3+2
        ax.append(fig.add_subplot(gs[ax1]))
        ax.append(fig.add_subplot(gs[ax2]))
        ax.append(fig.add_subplot(gs[ax3]))

        # Plot tracking
        ax[ax1].plot(trackData[:,0],trackData[:,1],colors[d])

        # Plot Y over time
        timePerFrame = 1./aviProps[4]
        timePerFrame = timePerFrame/60. # convert from seconds to minutes
        tAxis = np.arange(0, len(trackData)*timePerFrame, timePerFrame)
        if len(tAxis)>len(trackData): tAxis = np.delete(tAxis, -1)
        if len(tAxis)<len(trackData): trackData = np.delete(trackData, -1)
        smooth_trackData = smooth.smooth(trackData[:,1], window_len=50)
        ax[ax2].plot(tAxis, trackData[:,1],'k',lw=1)
        ax[ax2].plot(tAxis, smooth_trackData, colors[d], lw=1.5)

        # Plot histogram
        ax[ax3].hist(trackData[:,1], bins=30, orientation='horizontal', histtype='stepfilled', normed=True, color=colors[d])
        ax[ax3].set_xlim([0,0.008])

        # get and plot looms
        #loomOnsets = da.getLoomOnsets(trackData, aviProps)
        #for l in loomOnsets: ax[ax2].plot(l, 1150, marker='o', markerfacecolor='k', markeredgecolor='k')
    plt.show()
    return dataOut

# ------------------------------------------
data, props = [], []
for d in dirList:
    fname = d + '/trackingData.txt'
    movieFname = d + '/trackingMovie.avi'
    data.append(np.loadtxt(fname))
    props.append(va.getAVIinfo(fname))

dataOut = plotTrackingData(data, props)





