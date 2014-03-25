'''******************************************
display.py 

-Handles all video output
-Displays messages to user
-Displays final product to user


******************************************'''

import time
import pygame
import os
from PIL import Image

import my_globals
import imagemagick

#local collage variables
USING_COLLAGES = False #set to true if images exist in collages directory
COLLAGE_ITERATOR = 0 #counter for COLLAGE_PICTURES usage#verify image files exist in collages directory
#verify collage pictures exist
if(len(my_globals.COLLAGE_PICTURES) > 0):
	global USING_COLLAGES #declare global or can't modify value
	print("using collages: " + str(len(my_globals.COLLAGE_PICTURES)))
	#set using_collages variable to true
	USING_COLLAGES = True


def clearWindow():
	my_globals.content_window.fill((255,255,255))
	pygame.display.update()

def hideWindow():
	content_window = my_globals.initWindow(1,1)
def showWindow():
	content_window = my_globals.initWindow()


#display label in window centered on dimensions of window
#def blitWindow(window, label, center = True, pos = (0, 0)):
def blitWindow(label, center = True, pos = (0, 0)):
	#make window white
	#window.fill((255,255,255))
	if(center):
		textpos = getCenter(my_globals.content_window.get_width(), my_globals.content_window.get_height(), label)
		textpos = getCenter(my_globals.screenWidth, my_globals.screenHeight, label)
	else:
		textpos = pos
	my_globals.content_window.blit(label, textpos)
	pygame.display.update()


#function to ask user to press button to begin
def requestButtonToBegin():
	#request button window text string
	theText = "Press button to begin photo shoot!"
	displayContentText(theText, True)

def getCenter(width, height, object):
	textpos = object.get_rect(centerx=width/2, centery=height/2)
	return textpos

#get maximum font sizem for width/height constraint
def getMaxCharSize(width, height, text = '3'):
	#90% of width
	#width = width*0.9
	print("target width: " + str(width))
	print("target height: " + str(height))
	size = 10;
	while(True):
		x = pygame.font.Font(None, size).size(text)[0]
		y = pygame.font.Font(None, size).size(text)[1]
		if(x < width and y < height):
			size += 10
		else:
			#woah woah woah...back it up
			size -= 10
			break
	x = pygame.font.Font(None, size).size(text)[0]
	y = pygame.font.Font(None, size).size(text)[1]
	print("x:" + str(x))
	print("y:" + str(y))
	print("size: " + str(size))
	return size

#display @str message to user
def displayMessage(message_text, clearScreen = False):
	if(clearScreen):
		clearWindow()

	size = getMaxCharSize(my_globals.screenWidth, my_globals.message_height, message_text)
	#generate font for window
	myfont = pygame.font.Font(None, size)
	label = myfont.render(message_text, 1, (0,0,0))
	blitWindow(label, False, getCenter(my_globals.screenWidth, my_globals.message_height, label))

#function to display image in content area
def displayContentImage(content_obj, clearScreen = False):
	if(clearScreen):
		clearWindow()

	x = int((my_globals.screenWidth - content_obj.get_width())/2)
	y = my_globals.message_height + int((my_globals.content_height - content_obj.get_height())/2)
	blitWindow(content_obj, False, (x, y))

#function to display text in content area
def displayContentText(content_text, clearScreen = False):
	if(clearScreen):
		clearWindow()

	size = getMaxCharSize(my_globals.screenWidth, my_globals.content_height, content_text)
	myfont = pygame.font.Font(None, size)
	label = myfont.render(content_text, 1, (0,0,0))
	blitWindow(label, False, getCenter(my_globals.screenWidth, my_globals.screenHeight + my_globals.message_height, label))


#function to inform user the photo strip is being generated
#displays image collage to user so they have something to look at while waiting
def displayEntertainment():
	clearWindow()
	displayMessage("Compiling pictures into photo strip...")
	#verify we have entertainment ot display

	global COLLAGE_ITERATOR #otherwise get reference before assignment error
	global USING_COLLAGES #otherwise always is false

	if(USING_COLLAGES):
		print("using collages")
		file = my_globals.COLLAGE_PICTURES[COLLAGE_ITERATOR]
		print("file: " + file)
		#increment iterator
		COLLAGE_ITERATOR += 1
		#verify iterator didn't go past limit
		if(COLLAGE_ITERATOR >= my_globals.COLLAGE_ITERATOR_MAX):
			print("collage iterator set to 0 because iterator got to: " + str(COLLAGE_ITERATOR) + " which is greater than " + str(my_globals.COLLAGE_ITERATOR_MAX))
			#reset iterator if past max
			COLLAGE_ITERATOR = 0

		#verify file exists before displaying it to user
		if(os.path.isfile(file) == False):
			print("collage doesn't exist")
			#file doesn't exist, return
			return False

		#load image
		image = pygame.image.load(file)
		#display to user
		print("display to user")
		displayContentImage(image)
	


#take @id and display associated picture in content area
#scale picture width/height to fit constraints
def displayPhotoBoothPicture(id = ""):
	#prepare file name
	file = my_globals.PBOOTH_SETS + "complete_" + id + ".jpg"
	#load image
	image = pygame.image.load(file)
	#get dimensions of image
	w,h = pygame.Surface.get_size(image)
	#convert width/height to floats
	w = float(w)
	h = float(h)
	#calculate width of image that will fit in content area
	newWidth = float(((w / h) * my_globals.content_height))
	#scale image to fit content area width/height
	image = pygame.transform.scale(image, (int(newWidth), my_globals.content_height))
	#display image to user
	displayContentImage(image)
	