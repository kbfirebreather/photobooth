import pygame
import os


#directory for photo booth images
PBOOTH_DIR = "/home/pi/photobooth/images/"
PBOOTH_SETS = "/home/pi/photobooth/sets/"
PBOOTH_THUMBS = "/home/pi/photobooth/thumbs/"
PBOOTH_BOTTOM = "/home/pi/photobooth/"


#initialize pygame for graphics
pygame.init()
pygame.font.init()

#get current screen info (resolution)
screenInfo = pygame.display.Info()
screenWidth = screenInfo.current_w
screenHeight = screenInfo.current_h

screenPosX = int((screenWidth - screenHeight) / 2)
screenWidth = screenHeight



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
print("Availble content height: " + str(content_height))

#backround color for content window
currentBgColor = (255, 255, 255)
