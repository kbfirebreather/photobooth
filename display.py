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


def clearWindow():
	my_globals.content_window.fill((255,255,255))
	#my_globals.content_window.fill((0,0,0))
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

def getCenter(width, height, object):
	textpos = object.get_rect(centerx=width/2, centery=height/2)
	print(textpos)
	print(width)
	print(height)
	return textpos

#get maximum font size?
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

#display 3,2,1 countdown in top left corner of screen
def displayCountDown(countDownText = "Taking photo in "):
	#close request button push window
	#pygame.display.quit()
	#fill window white background
	my_globals.content_window.fill((255,255,255))
	#update window so user sees white background
	pygame.display.update()

	#request button window text string
	theText = countDownText + " 1";
	size = getMaxCharSize(my_globals.screenWidth, my_globals.message_height, theText)
	#generate font for countdown in window
	myfont = pygame.font.Font(None, size)
	label = myfont.render(theText, 1, (0,0,0))
	#show countdown from 3 to 1 in this loop
	for i in range(0, 3):
		clearWindow()
		countDown = 3-1*i
		#get time before clearing screen and displaying stuff
		time_before_display = time.time()
		displayContentText(str(countDown))
		displayMessage(countDownText)
		#displayMessage(str(countDown))
		#time after done updating display
		time_after_display = time.time()
		#calculate remaining time in "1 second" to wait until we go to the next second
		sleepfor = 1-(time_after_display - time_before_display)
		if(sleepfor < 0):
			sleepfor = 0;

		print("SLEEP: " + str(sleepfor))
		print(time_after_display)
		print(time_before_display)
		#blitWindow(label)
		time.sleep(sleepfor)
		clearWindow()

	print("Finished in " + str(time.time() - time_before_display))

#display @str message to user
def displayMessage(message_text, clearScreen = False):
	if(clearScreen):
		clearWindow()

	size = getMaxCharSize(my_globals.screenWidth, my_globals.message_height, message_text)
	#generate font for window
	myfont = pygame.font.Font(None, size)
	label = myfont.render(message_text, 1, (0,0,0))
	blitWindow(label, False, getCenter(my_globals.screenWidth, my_globals.message_height, label))

def displayContentImage(content_obj, clearScreen = False):
	if(clearScreen):
		clearWindow()
	print("size:::")
	print(content_obj.get_size())
	print(content_obj.get_width())
	print(content_obj.get_height())

	x = int((my_globals.screenWidth - content_obj.get_width())/2)
	y = my_globals.message_height + int((my_globals.content_height - content_obj.get_height())/2)
	#print(content_obj.size)
	#size = getMaxCharSize(my_globals.screenWidth, my_globals.content_height, content_obj)
	#myfont = pygame.font.Font(None, size)
	#label = myfont.render(content_obj, 1, (0,0,0))
	blitWindow(content_obj, False, (x, y))

def displayContentText(content_text, clearScreen = False):
	if(clearScreen):
		clearWindow()

	size = getMaxCharSize(my_globals.screenWidth, my_globals.content_height, content_text)
	myfont = pygame.font.Font(None, size)
	label = myfont.render(content_text, 1, (0,0,0))
	blitWindow(label, False, getCenter(my_globals.screenWidth, my_globals.screenHeight + my_globals.message_height, label))

def displayEntertainment():
	clearWindow()
	displayMessage("Compiling pictures into photo strip...")
	
	#file = my_globals.PBOOTH_THUMBS + "montage.jpg"
	file = my_globals.PBOOTH_BOTTOM + "big_preview.jpg"
	#don't show preview if big_preview.jpg doesn't exist
	if(os.path.isfile(file) == False):
		return False
	image = pygame.image.load(file)
	#image = pygame.transform.scale(image, (373,560))
	displayContentImage(image)
	#blitWindow(image, False, getCenter(my_globals.screenWidth, my_globals.screenHeight+200, image))
	#window_photobooth.blit(image, (0,0))
	#pygame.display.update()
	#time.sleep(5)
	



def displayPhotoBoothPicture(id = ""):
	file = my_globals.PBOOTH_SETS + "complete_" + id + ".jpg"
	#set starting point for next window to 0,0 (top left corner of screen)
	

	image = pygame.image.load(file)
	w,h = pygame.Surface.get_size(image)
	w = float(w)
	h = float(h)
	newWidth = float(((w / h) * my_globals.content_height))
	print("stuff here")
	print(w)
	print(h)
	print(newWidth)
	print(str(float(w/h)))
	print("global height: " + str(my_globals.content_height))
	image = pygame.transform.scale(image, (int(newWidth), my_globals.content_height))
	displayContentImage(image)
	#blitWindow(image, False, getCenter(my_globals.screenWidth, my_globals.screenHeight+200, image))
	#window_photobooth.blit(image, (0,0))
	#pygame.display.update()
	