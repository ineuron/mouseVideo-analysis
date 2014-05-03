# Library of functions for analysing .avi behaviour movies
# Tiago Branco - March 2014

# Import modules
import numpy as np
import matplotlib.pylab as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import matplotlib.cm as colormap
import scipy.ndimage as ndimage
import os.path
import cv2

#saveDir = '/lmb/home/tbranco/analysis/'

# Auxiliary functions
def getFileName(fname):
    directory, filename = os.path.split(fname)
    return filename

def writeDict(dic, filename):
    with open(filename, "w") as f:
        for i in dic.keys():            
            f.write(i + " :" + " ".join([str(x) for x in dic[i]]) + "\n")

def getAVIinfo(fname):
    cap = cv2.VideoCapture(fname)
    aviProps = []
    for prop in np.arange(1, 8):
        aviProps.append(cap.get(prop))
    cap.release()
    return aviProps #0-posFrame,1-posRatio,2-fWidth,3-fHeight,4-fps,5-fourcc,6-nFrames

def time2frame(t, aviProps):   # Time in seconds
    fps = aviProps[4]
    t = t*1000
    f = t/(1000/fps)
    return int(f)

def frame2time(f, aviProps):
    fps = aviProps[4]
    t = f/float(fps)
    return t

def erode(img, erosion_size):
    erosion_size = 2*erosion_size+1
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(erosion_size,erosion_size))
    eroded = cv2.erode(img,kernel)
    return eroded

def dilate(img, dilation_size):
    dilation_size = 2*dilation_size+1
    kernel =  cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(dilation_size,dilation_size))
    dilated = cv2.dilate(img,kernel)
    return dilated

def subtractBg(frame, bg):
    ibg = plt.invert(np.uint8(bg))
    iFrame = plt.invert(np.uint8(frame))
    bgSubFrame = np.int32(iFrame)-np.int32(ibg)
    return bgSubFrame    # returns inverted frame

def applyThreshold(frame, ths):
    frame[frame<ths] = 0
    ret,thsFrame = cv2.threshold(np.uint8(frame), ths, 255, cv2.THRESH_BINARY)
    return thsFrame

def showArena(aviProps, bg):
    frameWidth = aviProps[2]
    frameHeight = aviProps[3]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cmap = colormap.gray      
    im = ax.imshow(bg)
    cmap = colormap.gray
    im.set_cmap(cmap)
    ax.plot([],[])
    plt.ylim([frameHeight, 0])
    plt.xlim([0, frameWidth])
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    return fig, ax

def getDistance(pt1, pt2):
    d = np.sqrt(np.square(pt2[0]-pt1[0]) + np.square(pt2[1]-pt1[1]))
    return d

def is_inArea(pt, area): # Rectangular area
    W = area[1][0] - area[0][0]
    H = area[2][1] - area[1][1]
    x = (pt[0]>area[0][0]) & (pt[0]<area[0][0]+W)
    y = (pt[1]<area[0][1]) & (pt[1]>area[0][1]+H)
    if x & y:
        return True
    else:
        return False

# Preparation for processing functions
def getBg(fname, aviProps, nFrames):       
    if nFrames>aviProps[6]: nFrames=aviProps[6]
    cap = cv2.VideoCapture(fname)
    frames = np.zeros([aviProps[3],aviProps[2],nFrames])
    randomFrames = np.random.randint(aviProps[6], size=nFrames)
    for f in np.arange(0,nFrames):
        cap.set(1, randomFrames[f])
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frames[:,:,f] = gray
    #fileName = getFileName(fname)
    #fsaveName = saveDir + fileName.rstrip(".avi") + "_bg" 
    #np.save(fsaveName, frames.mean(axis=2))
    #cap.release()
    #print fsaveName, "saved"
    return frames.mean(axis=2)

def setThreshold(fname, aviProps, bg, ths, morphDiameter):    
    cap = cv2.VideoCapture(fname)
    sPlot = [221,222,223,224]
    nFrames = aviProps[6]
    frames = np.arange(0, nFrames, int(nFrames/4))
    fig = plt.figure()
    cmap = colormap.gray
    cmap.set_over('r')
    for f in np.arange(0,4):
        cap.set(1,frames[f])
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)      
        bgSubGray = subtractBg(gray, bg)        
        thsGray = applyThreshold(bgSubGray, ths)
        thsGray = erode(thsGray, morphDiameter)
        thsGray = dilate(thsGray, morphDiameter)
        gray[gray==255] = 254
        gray[thsGray==255] = 255
        cOm = ndimage.measurements.center_of_mass(thsGray)
        #if tFrame.sum()/255 < nestThreshold: cOm = nestPosition
        fig.add_subplot(sPlot[f])
        plt.imshow(gray, vmax=254)
        plt.set_cmap(cmap)
        plt.plot(cOm[1],cOm[0], 'o')
    cap.release()
    plt.show()
    return ths, morphDiameter

def setPoints(fname, aviProps, bg):
    frameWidth = aviProps[2]
    frameHeight = aviProps[3]
    fig, ax = showArena(aviProps, bg)

    # 1 point for nest position
    print "Set nest position [1 point]"
    nestPosition = fig.ginput(1)
    nestPosition = nestPosition[0]
    ax.plot(nestPosition[0],nestPosition[1], '+')
    fig.canvas.draw()

    # 4 points for nest area
    print "Set nest area [3 points: lower left, lower right, top]"
    nestArea = fig.ginput(3)
    W = nestArea[1][0] - nestArea[0][0]
    H = nestArea[2][1] - nestArea[1][1]
    rect = plt.Rectangle((nestArea[0][0],nestArea[0][1]),W,H, fc='r', alpha=0.2)
    ax.add_patch(rect)
    fig.canvas.draw()

    # 1 point for middle of arena
    print "Set centre of arena [1 point]"
    arenaCentre = fig.ginput(1)   
    arenaCentre = arenaCentre[0]
    x = [arenaCentre[0], arenaCentre[0]]
    y = [0,frameHeight-60]
    ax.plot(x,y, 'b')
    fig.canvas.draw()

    # 2 points for feeding area
    print "Set feeding area [3 points: lower left, lower right, top]"
    feedingArea = fig.ginput(3)   
    #circle = plt.Circle((feedingArea[0][0],feedingArea[0][1]), radius=feedingArea[1][0]-feedingArea[0][0], fc='c')
    #ax.add_patch(circle)
    W = feedingArea[1][0] - feedingArea[0][0]
    H = feedingArea[2][1] - feedingArea[1][1]
    rect2 = plt.Rectangle((feedingArea[0][0],feedingArea[0][1]),W,H, fc='c', alpha=0.2)
    ax.add_patch(rect2)
    fig.canvas.draw()

   pts = [nestPosition, nestArea, arenaCentre, feedingArea]
    #fsaveName = fname.rstrip(".avi") + "_arena"
    #np.save(fsaveName, ths)
    #print fsaveName, "saved"
    return pts

def plotArena(aviProps, pmts, bg):
    frameWidth = aviProps[2]
    frameHeight = aviProps[3]
    fig, ax = showArena(aviProps, bg)
    fig.show() 

    nestPosition, nestArea, arenaCentre, feedingArea = pmts[2], pmts[3], pmts[4], pmts[5]
    ax.plot(nestPosition[0],nestPosition[1], '+')
    W = nestArea[1][0] - nestArea[0][0]
    H = nestArea[2][1] - nestArea[1][1]
    rect = plt.Rectangle((nestArea[0][0],nestArea[0][1]),W,H, fc='r', alpha=0.2)
    ax.add_patch(rect)
    x = [arenaCentre[0], arenaCentre[0]]
    y = [0,frameHeight-60]
    ax.plot(x,y, 'b')
    W = feedingArea[1][0] - feedingArea[0][0]
    H = feedingArea[2][1] - feedingArea[1][1]
    rect2 = plt.Rectangle((feedingArea[0][0],feedingArea[0][1]),W,H, fc='c', alpha=0.2)
    ax.add_patch(rect2)
    fig.canvas.draw()


# Processing functions
def processFrames(fname, aviFname, aviProps, tStart, tEnd, bg, pmts, nestThreshold, saveAVI=False):   # Time in seconds
    startFrame = time2frame(tStart, aviProps)
    endFrame = time2frame(tEnd, aviProps)
    if endFrame>aviProps[6]: endFrame=aviProps[6]
    ths = pmts[0][0]
    morphDiameter = pmts[1][0]
    nestPosition = (pmts[2][1],pmts[2][0])
    fileName = getFileName(fname)

    # Start cv2 object
    cap = cv2.VideoCapture(fname)
    cap.set(1, startFrame)
    if saveAVI:
        fourcc = cv2.cv.FOURCC('X','V','I','D')
        out = cv2.VideoWriter(aviFname, fourcc, aviProps[4], (int(aviProps[2]), int(aviProps[3]))) 

    mousePositions, mouseSize = [], []
    for f in np.arange(startFrame, endFrame):
        # Read frame
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Process frame
        bgSubGray = subtractBg(gray, bg)        
        thsGray = applyThreshold(bgSubGray, ths)
        thsGray = erode(thsGray, morphDiameter)
        thsGray = dilate(thsGray, morphDiameter)
        frame[thsGray==255,1] = 255
        mouseSize.append(thsGray.sum())
        if thsGray.sum()==0: #/255 < nestThreshold:
            if f==startFrame:
                curPos = nestPosition
            else:
                curPos = mousePositions[-1] 
            mousePositions.append(curPos)  # Mouse is in the nest or in outer space looking for George Clooney
            frame[curPos[0]-5:curPos[0]+5,curPos[1]-5:curPos[1]+5,1] = 153
        else:
            cOm = ndimage.measurements.center_of_mass(thsGray)
            mousePositions.append(cOm)
            frame[cOm[0]-5:cOm[0]+5,cOm[1]-5:cOm[1]+5,1] = 153
        if saveAVI: out.write(frame)
    cap.release()
    out.release()
    mouseSize = np.array(mouseSize)
    mouseSize.shape = (len(mouseSize),1)
    dataOut = np.hstack((np.array(mousePositions), mouseSize))
    #fsaveName = saveDir + fileName.rstrip(".avi") + "_trackingData"
    #np.save(fsaveName, dataOut)
    #print fsaveName, "saved"
    return dataOut

def analyseData(fname, aviProps, bg,  pmts, PLOT=True):
    data = np.loadtxt(fname)
    fps = aviProps[4]    
    fileName = getFileName(fname)

    # Total distance travelled
    dist = []
    for n in np.arange(0,len(data)-1):
        dist.append(getDistance(data[n], data[n+1]))
    distSum = np.sum(dist)

    # Time spend in each area
    secPerFrame = 1./fps
    nest = pmts[3]
    food = pmts[5]
    mouseSize = 500000
    nestCounter, foodCounter, leftCounter, rightCounter = 0, 0, 0, 0
    arena = []
    for n in data:
        if is_inArea((n[1],n[0]), nest): nestCounter+=secPerFrame
        if is_inArea((n[1],n[0]), food): foodCounter+=secPerFrame
        if n[1]<pmts[4][0]:
            leftCounter+=secPerFrame
        else:
            rightCounter+=secPerFrame
        if (is_inArea((n[1],n[0]), nest)==False) & (n[2]>mouseSize): 
            arena.append(1)
        else:
            arena.append(0)

    # Exploratory runs
    runsLabel = []
    r, i = 0, 0
    while i<len(arena):
        if arena[i]==1:
            r+=1       
            while i<len(arena) and arena[i]==1:
                runsLabel.append(r)
                i+=1
        else:
            runsLabel.append(0)
            i+=1

    runs = []
    runsLabel = np.array(runsLabel)
    for n in np.arange(1, np.max(runsLabel)+1):
        runs.append(data[runsLabel==n])

    runsDistance, runsTime = [], []
    for r in runs:
        dist = []
        for p in np.arange(0, len(r)-1):
            dist.append(getDistance(r[p],r[p+1]))
        runsDistance.append(np.sum(dist))
        runsTime.append(len(r)*secPerFrame)
        
    # Plot trajectory
    if PLOT:
      fig, ax = showArena(aviProps, bg)
      #ax.plot(data[:,1], data[:,0])
      for n in np.arange(0, len(runs)):
          ax.plot(runs[n][:,1], runs[n][:,0])
      #plt.show()
      

    results = [distSum, nestCounter, foodCounter, leftCounter, rightCounter, runsDistance, runsTime]
    resultsDict = {'Total distance':[distSum], 'Nest time':[nestCounter], 'FoodArea time':[foodCounter], 'Left side time':[leftCounter], 'Right side time':[rightCounter], 'Number of runs':[len(runs)], 'Distance per run':[runsDistance], 'Time per run':[runsTime]}     
    #fsaveName = saveDir + fileName.rstrip("_trackingData.npy") + "_trackingDataProcessed.txt"
    #writeDict(resultsDict, fsaveName)
    #print fsaveName, "saved"
    return data, resultsDict, fig




