'''******************************************
booth.py 

-Main python program that hooks everything together


******************************************'''

import sys
import os
import pygame
import pdb
import numpy
import array
import time
import time
import thread
import threading
import signal
import re
import math


import my_globals
import display
import imagemagick
import gpio_handler
import ink_levels

PRINT_PICTURES = False


#create thread for checking ink levels
thread_ink_levels = threading.Thread(target=ink_levels.checkInkLevelThread, args=[])
print("Starting ink level checking thread...")
#start ink level checking thread
#######################################################################################thread_ink_levels.start()


#setup signal handler to catch ctrl+c detection and exit cleanly
def signal_handler(signal, frame):
	print("Ctrl+C detected...")
	print("Cleaning up GPIO...")
	gpio_handler.exit()
	print("Notifying ink level thread to exit...")
	ink_levels.killThread = True
	thread_ink_levels.join()
	print("Exiting...")
	sys.exit(0)
#set signal handlder
signal.signal(signal.SIGINT, signal_handler)




#function to send picture to printer
def printPicture(number):
	#temporary variable check so we don't print accidentally
	if(not PRINT_PICTURES):
		return False

	file = "/home/pi/photobooth/sets/complete_" + number + ".jpg"
	command = "lpr " + file
	imagemagick.cmd_line(command)





#function to ask user to press button to begin
#should this be moved to display.py?
def displayRequestButtonWindow():
	#request button window text string
	theText = "Press button to begin photo shoot!"
	display.displayContentText(theText, True)


#function Take photo and save to @filename
def takePhoto(filename):
	#append filename to global photobooth image directory
	filename = my_globals.PBOOTH_DIR + filename
	#command line instruction to take picture with camera after 3 seconds
	cmdline = "raspistill -fp -t 3000 -o " + filename
	#send command to command line
	os.system(cmdline)



#use image magick to create photobooth picture to print out
#should this me moved to imagemagick.py?
def makePhotoBoothPicture(startingPictureNumber, filenames, filethumbs, convert_threads):

	#images = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg']
	#random.shuffle(images)
	print("image magick time")
	print(imagemagick.montage(filenames, filethumbs, convert_threads, str(startingPictureNumber)))



#user pressed button so now we'll go through entire photo booth sequence
#function that runs after user presses button to run photobooth sequence
def runPhotoBooth():
	#clear content space to work wirth
	display.clearWindow()

	#need name of photo set that dictates beginning of photo filenames
	name = "photobooth"

	#starting number for photo set
	pic_num = 1
	#inform user that the system will take 4 pictures
	display.displayMessage("The system will now take 4 consecutive pictures.")
	#wait 3 seconds
	time.sleep(3)


	pic_num = int(my_globals.STARTING_PIC_NUM)
	starting_num = pic_num

	#threads for resizing photos to 800x600
	convert_threads = []
	small_thumb_threads = []

	filenames = []
	filethumbs = []
	counter = 0
	#while(pic_num < 5):
	#hide display some how?
	#display.clearWindow()
	#display.hideWindow()

	#display.displayContentText("Picture " + str(counter+1), True)
	while(counter <= 3):#3):
		display.showWindow()
		display.displayContentText("Picture " + str(counter+1), True)
		time.sleep(1)
		#setup filename to be saved
		filename = name + "_" + str(pic_num) + ".jpg"
		filethumb = "thumb_" + filename
		filenames.append(filename)
		filethumbs.append(filethumb)
		#displayMessage("Taking photo " + str(pic_num) + " out of 4")
		t1 = threading.Thread(target=takePhoto, args=[filename])

		#start countdown thread
		gpio_handler.countdownThread()
		t1.start()
		time.sleep(1)
		display.clearWindow()
		t1.join()
		#takePhoto(filename)
		#t1.start()

		display.clearWindow()
		#display.displayCountDown("Taking photo " + str(counter + 1))
		print("display countdown to 7 segment LED")
		#wait for photo taking thread to complete
		#t1.join()
		#print("length:::: " + str(done - now))
		display.hideWindow()
		#photo is now taken by piCamera
		#use 'epeg' to shrink it to 800x600 in a thread
		#this is done so imagemagick runs quicker on a smaller file
		convert_s = "epeg -m 800,600 -q 100 " + my_globals.PBOOTH_DIR+filename + " -q 100 " + my_globals.PBOOTH_THUMBS+filethumb
		convert_threads.append(threading.Thread(target=imagemagick.cmd_line, args=[convert_s]))
		convert_threads[counter].start()
		#use epeg to shrink picture even smaller for thumbnail collage
		#epeg_thumb = "epeg -m 107,128 -q 100 " + my_globals.PBOOTH_DIR+filename + " -q 100 " + my_globals.PBOOTH_THUMBS+filethumb
		#small_thumb_threads.append(threading.Thread(target=imagemagick.cmd_line, args=[epeg_thumb]))
		#small_thumb_threads[counter].start()

		#increment pic num for next one
		pic_num = pic_num + 1
		counter = counter + 1

	display.showWindow()

	#bring display back?
	#my_globals.content_windwo = my_globals.initWindow()

	#update starting pic num in my_globals to new value
	my_globals.STARTING_PIC_NUM = str(pic_num)

	#entertain user...
	display.displayEntertainment()
	
	wait_threads_time = makePhotoBoothPicture(starting_num, filenames, filethumbs, convert_threads)
	
	display.clearWindow()

	#display photo booth picture to user

	display.displayMessage("Here is the result! Press the button if you would like a redo!", True)
	#show picture to user
	display.displayPhotoBoothPicture(str(starting_num))
	#for 5 seconds
	time.sleep(5)
	printPicture(str(starting_num))
	display.displayMessage("Printing picture! Please allow a minute or two for the print to begin!", True)
	display.displayPhotoBoothPicture(str(starting_num))
	time.sleep(7)


def mainLoop():
	#fps = 30
	#clock = pygame.time.Clock()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		#pygame.display.update()
		#clock.tick(fps)

		if(gpio_handler.isButtonPressed()):
			#run this in a thread
			runPhotoBooth()
			#photobooth finished, display request to user to hit button to begin again
			displayRequestButtonWindow()


if __name__ == "__main__":
	#verify we have printer access
	while(ink_levels.checkInkLevel() == False):
		display.displayContentText("Unable to access printer. Please toggle printer power.", True)
		time.sleep(1)
	#display request to user to hit buton
	displayRequestButtonWindow()
	#run indefinite main loop
	mainLoop()
	