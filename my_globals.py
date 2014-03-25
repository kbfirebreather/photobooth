'''******************************************
my_globals.py 

-Global Variables for use throughout entire program
	-directories for use in program
	-Screen dimensions

-Initializes pygame window


******************************************'''

import pygame
import os
import sys
import time
import glob #for finding files in directory
import threading #for locking

#directory for photo booth images
PBOOTH_DIR = "/home/pi/photobooth/images/"
PBOOTH_SETS = "/home/pi/photobooth/sets/"
PBOOTH_THUMBS = "/home/pi/photobooth/thumbs/"
PBOOTH_BOTTOM = "/home/pi/photobooth/"
PBOOTH_COLLAGES = "/home/pi/photobooth/collages/"

#collage usage variables
COLLAGE_PICTURES = glob.glob(PBOOTH_COLLAGES + "*.jpg") #list of images in collages directory
COLLAGE_ITERATOR_MAX = len(COLLAGE_PICTURES) #maximum limit for COLLAGE_PICTURES list

#lock for use with ink level checking thread and blocking gpio button detection
thread_lock = threading.Lock()

#initialize pygame for graphics
pygame.init()
pygame.font.init()

#get current screen info (resolution)
screenInfo = pygame.display.Info()
screenWidth = screenInfo.current_w
screenHeight = screenInfo.current_h

screenPosX = int((screenWidth - screenHeight) / 2)
screenWidth = screenHeight

#starting number for pictures taken by camera
STARTING_PIC_NUM = "1"

def initWindow(width = int(screenWidth), height = int(screenHeight)):
	#diffWidth = screenWidth - screenHeight
	#startLeft = diffWidth/2
	#width = height

	#set starting point for next window to 0,0 (top left corner of screen)
	os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (screenPosX,0)
	return pygame.display.set_mode((width, height), pygame.NOFRAME)


#os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (int(screenWidth*.10),int(screenHeight*.10))
#create window on screen that spans entier width and height of 200px
#message_window = pygame.display.set_mode((screenWidth, 200), pygame.NOFRAME)
#content_window = pygame.display.set_mode((int(screenWidth*0.90), int(screenHeight*0.90)), pygame.NOFRAME)
content_window = initWindow()

#message area height in content window
message_height = 125
#content area height in content window
content_height = screenHeight - message_height
#print("Availble content height: " + str(content_height))

#backround color for content window
currentBgColor = (255, 255, 255)



#determine if pictures have been taken previously so we can update starting picture number
#check all the image files in the image file directory
#this is for determining where to start picture numbering so we don't overwrite pictures already taken
#put all files from PBOOTH_DIR into img_files list
img_files = os.listdir(PBOOTH_DIR)
#update STARTING_PIC_NUM to number of files in directory + 1 if files exist in directory
#if no files exist, then the STARTING_PIC_NUM will stay at default of "1"
if(len(img_files) > 0):
	STARTING_PIC_NUM = str(len(img_files) + 1)


	