# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 00:07:13 2021

@author: ammo5
"""
# -------------------------------------
# Import necessary scientific packages
# -------------------------------------
import numpy as np

# --------------------------------------
# Setting universal plotting parameters
# --------------------------------------

# Set some appearance parameters that will apply to all figures defined in the code
import matplotlib as mpl

mpl.rcParams['lines.linewidth'] = 1.0
# mpl.rcParams['text.usetex'] = True # Not working right now
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = 'Times'
import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')
# ------------------------------------------------------------
# Define parameters for extracting images from the video file
# ------------------------------------------------------------

# Idenfity the directory containing the optical video file
import os

dataDirectory = os.getcwd()

4

# Define some parameters for reading and displaying images from the optical video
file =[]#list of all files to be used in video plotting loop
# file0kv=str(dataDirectory + '/102918sh390mmTemp150KV0R_201811_2059.avi')  # location and name of the video file, to be appended to list
# file.append(file0kv)#add location to list
# file2kv=str(dataDirectory + '/102918sh390mmTemp150KV2R_201811_2152.avi')  # location and name of the video file, to be appended to list
# file.append(file2kv)#add location to list
# file4kv=str(dataDirectory + '/102918sh390mmTemp150KV4R_201811_2214.avi')  # location and name of the video file, to be appended to list
# file.append(file4kv)#add location to list
# file6kv=str(dataDirectory + '/102918sh390mmTemp150KV6R_201811_2245.avi')  # location and name of the video file, to be appended to list
# file.append(file6kv)#add location to list
file8kv=str(dataDirectory + '/Temp150KV8.avi')  # location and name of the video file, to be appended to list
file.append(file8kv)#add location to list
# file10kv=str(dataDirectory + '/102918sh390mmTemp150KV10R_201811_1456.avi')  # location and name of the video file, to be appended to list
# file.append(file10kv)#add location to list

fps = 7000  # frame rate of optical video, uniform for every video
firstFrame = [31,28,33,31,33,34] # list of first frame of each video, dependent on first frame where droplet fully enters camera
lastFrame = [ff+200 for ff in firstFrame]  # uniform last frame of each video, dependent on same time stamp
Nframes = 2  # number of frames we wish to display
deltaframe=[]#empty deltaframe list
zip_frame=zip(firstFrame,lastFrame)
for firstFrame_i, lastFrame_i in  zip_frame:
    dframe=(lastFrame_i - firstFrame_i) / (Nframes - 1)
    deltaframe.append(dframe)#calculate deltaframe with both first and last frame
frame = np.zeros(Nframes)  # initialize array containing frame numbers to be displayed
deltalocator=0 #variable to select right variable in deltaframe list
for FF in firstFrame:
    for i in np.arange(Nframes):
        frame[i] = int(FF + (i+1) * deltaframe[deltalocator])  # calculate frame numbers to be displayed
    deltalocator+=1

time = (frame - firstFrame[0]) / fps * 1e3  # time elapsed is uniform for all videos

# Define points for cropping the video image (points measured in ImageJ)
xBottom = 512  # bubble nucleation spot (x location)
yBottom = 512  # bubble nucleation spot (y location)
#x1 = xBottom - 512
x1=300
x2=1024-100
y1=500
y2=950
#x2 = xBottom + 512
#y2 = yBottom + 512
#y1 = y2 - 512

# -------------------------------------------------------
# Read images from the video and insert them in a figure
# -------------------------------------------------------
import cv2 as cv  # package for reading video files

import matplotlib.pyplot as plt  # package for drawing figures
plotLevel=1 #used to move plot for each file so all can be displayed
fig = plt.figure(1, figsize=(20*.4,12*.4))
for singleFile in file:
    cap = cv.VideoCapture(singleFile)  # read video from the video file
    frameCount = 1  # counter initialization
    i = 0  # counter initialization
    while (cap.isOpened()):  # loop through all the frames in the video
        ret, capFrame = cap.read()  # read a single frame image from the video
        if frameCount == frame[i]:  # check if this frame needs to be displayed
            frameImage = capFrame[y1:y2, x1:x2]  # crop the image
            ax = fig.add_subplot(4, 6, plotLevel)  # add a subplot in the figure
            img = ax.imshow(frameImage)  # display the image in the subplot
            kV=(plotLevel-1)*2
            img.set_cmap('gist_gray')  # Set the color mode of the displayed image
            ax.text(0, -14, 't = ' '%.1f ms' % time[i], color='black', fontsize=8)
            ax.text(180, -100, str(kV) + 'kV', color='black', fontsize=8)  # display time associated with image

            ax.set_axis_off()  # these three commands hide the x,y axis in the plot
            ax.axes.get_xaxis().set_visible(False)
            ax.axes.get_yaxis().set_visible(False)
            i = i + 1  # increment the counter
            if i == len(frame):  # check if all frames have been displayed
                break
        frameCount = frameCount + 1  # increment the counter
        if (ret == False):
            break
    cap.release()  # release the variable containing the video
    cv.destroyAllWindows()
    fig.show()  # display the figure
    plotLevel+=1

#code requires one repitition to create zoomed in line due to significantly different parameters
    zoomfile=[file8kv]
plotLevel=1 #used to move plot for each file so all can be displayed
fig = plt.figure(1, figsize=(20*.4,12*.4))
for singleFile in zoomfile:
    cap = cv.VideoCapture(singleFile)  # read video from the video file
    frameCount = 1  # counter initialization
    i = 0  # counter initialization
    while (cap.isOpened()):  # loop through all the frames in the video
        ret, capFrame = cap.read()  # read a single frame image from the video
        if frameCount == frame[i]:  # check if this frame needs to be displayed
            frameImage = capFrame[y1:y2, x1:x2]  # crop the image
            ax = fig.add_subplot(1, 2, plotLevel)  # add a subplot in the figure
            img = ax.imshow(frameImage)  # display the image in the subplot
            if plotLevel == 1:
                kV=2
            else:
                kV=8
            img.set_cmap('gist_gray')  # Set the color mode of the displayed image
            ax.text(260, 520, 't = ' '%.1f ms' % time[i], color='black', fontsize=8)
            ax.text(260, 480, 'Zoomed in ' + str(kV) + 'kV', color='black', fontsize=8)  # display time associated with image
            ax.set_axis_off()  # these three commands hide the x,y axis in the plot
            ax.axes.get_xaxis().set_visible(False)
            ax.axes.get_yaxis().set_visible(False)
            i = i + 1  # increment the counter
            if i == len(frame):  # check if all frames have been displayed
                break
        frameCount = frameCount + 1  # increment the counter
        if (ret == False):
            break
    cap.release()  # release the variable containing the video
    cv.destroyAllWindows()
    fig.show()  # display the figure
    plotLevel+=1












# Save the figure as a file (as .eps or .png or .jpg etc.)
fig.savefig('figure3.0.png', bbox_inches='tight', pad_inches=0.0, dpi=300 )#frameon=True
