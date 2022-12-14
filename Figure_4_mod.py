# -*- coding: utf-8 -*-
"""
Spyder Editor
Eletric Drop Project
Figure 4 - 0 & 8 kV
09/22/2021
Aramis Kelkelyan
"""
#-------------------------------------
# Import necessary scientific packages
#-------------------------------------
import numpy as np

#--------------------------------------
#Line 18-53: Setting universal plotting parameters
#--------------------------------------

# Set some appearance parameters that will apply to all figures defined in the code
import matplotlib as mpl
mpl.rcParams['lines.linewidth'] = 2.0
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = 'Times'
mpl.rcParams['axes.titlesize'] = 24

#------------------------------------------------------------
# Define parameters for extracting images from the video file
#------------------------------------------------------------

# Idenfity the directory containing the optical video file
import os
dataDirectory = os.getcwd()

# Define parameters for displaying images from the 0kV and 8kV video
file1 = str(dataDirectory+'/LongTemp150KV0.avi') # location and name of the video 0kV file
file2 = str(dataDirectory+'/LongTemp150KV8.avi') # location and name of the video 8kV file
files = [file1,file2]
fps = 7000 # frame rate of optical video
frame1 = np.array([13,273,443,640,805,920]) #805, 918, 1155, 1287, 1784, 1872 for 0kV
frame2 = np.array([14,93,114,237,387,635]) #for 8kV interesting frames include: 93, 114, 237, 387, 635, 1118, 1227
frames = [frame1,frame2] 
act_frame1 = np.array([5180,6485,7335,8320,9145,9720])
act_frame2 = np.array([9803,10198,10303,10918,11668,12908])
act_frames = [act_frame1,act_frame2]
time1 = (act_frame1 - act_frame1[0])/fps*1e3 # time elapsed (in ms) from the first frame (for frames to be displayed)
time2 = (act_frame2 - act_frame2[0])/fps*1e3 # time elapsed (in ms) from the first frame (for frames to be displayed)
times = [time1,time2]

# Define points for cropping the video image (points measured in ImageJ)
xBottom = 600 # bubble nucleation spot (x location)
yBottom = 500 # bubble nucleation spot (y location)
x1 = xBottom - 350
x2 = xBottom + 350
y2 = yBottom + 600
y1 = y2 - 1000

# Bubble length calibration (pixels/mm)
bubCalib1 = 3.25e-3/236
bubCalib2 = 3.25e-3/240
bubCalib = (bubCalib1 + bubCalib2)/2

# Shared scale bar parameter values

bubBarLocation = 'upper right' # location of scale bar on bubble image
bubBarSep = 2 # distance from edge of image
scaleBarFont = {'family': 'serif', # scale bar font settings
        'size': 4
        }

#-------------------------------------------------------
# Read images from the video and insert them in a figure
#-------------------------------------------------------
import cv2 as cv # package for reading video files
import matplotlib.pyplot as plt # package for drawing figures
from matplotlib_scalebar.scalebar import ScaleBar

for ii in range(len(frames)):

    fig = plt.figure(1, figsize=(6.5,2.5))
    frame = frames[ii]
    act_frame = act_frames[ii]
    time = times[ii]
    cap = cv.VideoCapture(files[ii]) # read video from the video file
    frameCount = 1 # frame counter initialization
    jj = 0 # subplot counter initialization
    
    while(cap.isOpened()): # loop through all the frames in the video (captures frame by frame)
        ret, capFrame = cap.read() # read a single frame image from the video 
        if frameCount == frame[jj]: # check if this frame needs to be displayed
            frameImage = capFrame[y1:y2, x1:x2] # crop the image

            if ii==0 and jj<6:
                ax = fig.add_subplot(2, 6, jj+1) # add a subplot in the figure
                ax.set_axis_off() # these three commands hide the x,y axis in the plot
                ax.axes.get_xaxis().set_visible(False)
                ax.axes.get_yaxis().set_visible(False)
            if ii==1 and jj<6:
                ax = fig.add_subplot(2, 6, jj+7) # add a subplot in the figure
                ax.set_axis_off() # these three commands hide the x,y axis in the plot
                ax.axes.get_xaxis().set_visible(False)
                ax.axes.get_yaxis().set_visible(False)
                
            if frameCount == frame1[0]:
                ax.text(-350, 500,'0kV', color='black', weight = 'bold', fontsize=10)
            
            if frameCount == frame2[0]:
                ax.text(-350, 500,'8kV', color='black', weight = 'bold', fontsize=10)
                
            img = ax.imshow(frameImage) # display the image in the subplot
            img.set_cmap('gist_gray') # Set the color mode of the displayed image            
           
            # define the scalebar
            scalebar = ScaleBar(bubCalib, length_fraction=0.4, height_fraction=0.05, 
                                location=bubBarLocation, pad=0.2, border_pad=0.0, sep=bubBarSep, 
                                frameon=False, color='white', box_color='white', box_alpha=1.0,
                                font_properties=scaleBarFont)
            # draw the scalebar
            ax.add_artist(scalebar)
            ax.text(135, -20,'%3.1f ms' %time[jj], color='black', fontsize=7) # display time associated with image
            jj=jj+1 # increment the counter
            if jj==len(frame): # check if all frames have been displayed
                break
        frameCount=frameCount+1 # increment the counter
        if(ret == False):
            break
    cap.release() # release the variable containing the video
    cv.destroyAllWindows()
    ii = ii + 1

fig.show() # display the figure

# Save the figure as a file (as .eps or .png or .jpg etc.)
fig.savefig('Figure_4mod.png', bbox_inches='tight', pad_inches=0.0, dpi=300) #frameon=True
