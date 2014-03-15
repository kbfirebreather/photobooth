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


'''******************************************
booth.py 

-Main python program that hooks everything together


******************************************'''

thread_ink_levels = threading.Thread(target=ink_levels.checkInkLevelThread, args=[])
print("Starting ink level checking thread...")
thread_ink_levels.start()

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


img_files = []

os.chdir(my_globals.PBOOTH_DIR)
for files in os.listdir("."):
	if(file == "out.jpg" or files == "complete.jpg" or files == "bottom_300dpi.jpg"):
		continue

	img_files.append(files)
	#print files

#print img_files

img_files = sorted(img_files)

'''
montage = "montage "
for x in range(0, len(img_files)):
	string = "epeg -m 107,128 -q 100 " + img_files[x] + " -q 100 " + my_globals.PBOOTH_THUMBS + "small_thumb_" + img_files[x]
	#print(string)
	#os.system(str)
	montage = montage + my_globals.PBOOTH_DIR + img_files[x] + " -resize"

#print img_files
#verify enough files for this to happen
os.chdir(my_globals.PBOOTH_THUMBS)
counter = 0

rows = 8
cols = 9

montage = "montage -geometry +1+1 -tile " + str(cols) + "x" + str(rows) + " -background '#0000FF' -alpha Opaque "
num_pics = 0;
for files in os.listdir("."):
	montage = montage + my_globals.PBOOTH_THUMBS + files + " "
	counter += 1
	num_pics += 1
	if(counter > cols*rows):
		print("counter > " + str(cols*rows))
		break;

montage = montage + " big_preview.jpg"
print(montage)

if(num_pics > 0):
	os.system(montage)

'''


def printPicture(number):
	file = "/home/pi/photobooth/sets/complete_" + number + ".jpg"
	command = "lpr " + file
	imagemagick.cmd_line(command)


#sys.exit(0)
#print(img_files)
#sys.exit(0)

#determine starting file number to use
#check amount of pictures already taken
#increment by 1
if(len(img_files) > 0):
	''' -- this is old code, probably not necessary anymore
	finalfile = img_files[len(img_files) - 1]
	replaced = re.sub('photobooth2_|thumb_photobooth2_|.jpg', '', finalfile)
	replaced = str((int(replaced) + 1))
	STARTING_NUM = replaced
	'''
	#pictures exist, starting number is num_pics+1
	STARTING_NUM = str(len(img_files) + 1)
else:
	#no pictures, starting number is at beginnign -- '1'
	STARTING_NUM = "1"


#print("STARTINGNUM: " + str(STARTING_NUM))
#gpio_handler.exit()
#sys.exit(0)


def displayRequestButtonWindow():
	#request button window text string
	theText = "Press button to begin photo shoot!"
	display.displayContentText(theText, True)


#Take photo and save to @filename
def takePhoto(filename):
	filename = my_globals.PBOOTH_DIR + filename
	cmdline = "raspistill -w 600 -h 600 -fp -op 125 -t 3000 -o " + filename
	#cmdline = "raspistill -w 600 -h 600 -f -p <0, 0, 640, 680> -t 3000 -o " + filename
	cmdline = "raspistill -fp -op 200 -t 3000 -o " + filename
	#cmdline = "raspistill -fp -w 1000 -h 1000 -t 3000 -o " + filename
	
	cmdline = "raspistill -fp -t 3000 -o " + filename
	
	#cmdline = "picture" + filename
	#print("cmd: " + cmdline)
	#take photo
	os.system(cmdline)



#use image magick to create photobooth picture to print out
def makePhotoBoothPicture(startingPictureNumber, filenames, filethumbs, convert_threads):

	#images = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg']
	#random.shuffle(images)
	print("image magick time")
	print(imagemagick.montage(filenames, filethumbs, convert_threads, str(startingPictureNumber)))



#user pressed button so now we'll go through entire photo booth sequence
def runPhotoBooth():
	#clear content space to work wirth
	display.clearWindow()

	start_time = time.time()

	#need this global declaration or else references won't work right
	global STARTING_NUM
	#need name of photo set
	name = "photobooth2"
	#starting number for photo set
	pic_num = 1
	display.displayMessage("The system will now take 4 consecutive pictures.")
	time.sleep(3)


	pic_num = int(STARTING_NUM)
	starting_num = pic_num

	convert_threads = []
	small_thumb_threads = []

	filenames = []
	filethumbs = []
	counter = 0
	#while(pic_num < 5):
	start_taking_pictures = time.time()
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

		now = time.time()
		#start countdown thread
		gpio_handler.countdownThread()
		t1.start()
		time.sleep(1)
		display.clearWindow()
		t1.join()
		#takePhoto(filename)
		done = time.time()
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

	end_taking_pictures = time.time()

	STARTING_NUM = str(pic_num)

	display.displayEntertainment()
	#entertain user...
	start_montage_time = time.time()
	wait_threads_time = makePhotoBoothPicture(starting_num, filenames, filethumbs, convert_threads)
	end_montage_time = time.time()
	display.clearWindow()

	#display photo booth picture to user


	#print("It took " + str(wait_threads_time) + " seconds to wait for the threads to complete")
	#print("It took " + str(end_montage_time - start_time) + " seconds to complete everything")
	#print("It took " + str(end_taking_pictures - start_taking_pictures) + " seconds to complete taking the pictures")
	#print("It took " + str(end_montage_time - start_montage_time) + " seconds to for the user to wait for pictures to be montaged")

	display.displayMessage("Here is the result! Press the button if you would like a redo!", True)
	#show picture to user
	display.displayPhotoBoothPicture(str(starting_num))
	#for 5 seconds
	time.sleep(5)
	printPicture(str(starting_num))
	display.displayMessage("Printing picture! Please allow a minute or two for the print to begin!", True)
	display.displayPhotoBoothPicture(str(starting_num))
	time.sleep(7)





#display request to user to hit buton
displayRequestButtonWindow()
#imagemagick.generate_preview()

#main loop
#time1 = time.time()
#5 minutes (60 seconds/  min * 5 minutes)
#update_delay = 60*5
#update_delay = 60*1 #1 minute

fps = 30
clock = pygame.time.Clock()
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
	#time2 = time.time()

	#update display every x minutes
	#check if we reached time
	'''
	if((time2 - time1) > update_delay):
		print("we reached delay, update display")
		#reset time stamp for checking
		time1 = time.time()
		#display same message to user
		displayRequestButtonWindow()
	'''

	pygame.display.update()
	clock.tick(fps)


	if(gpio_handler.isButtonPressed()):
		time1 = time.time()
		#run this in a thread
		runPhotoBooth()
		displayRequestButtonWindow()


################### DOESN'T GET PAST HERE





# doesn't stop running
# wait for user to press button and then take action
counter = 0
counter2 = 0
t1 = threading.Thread()
t1_running = False
#while True:
while (counter <= 3):
	if(isButtonPressed() == False and counter < 3):
		counter = counter+1
		continue;
	else:
		counter = 0
		counter2 += 1
		#counter = counter+1
		print("Button pushed, let's take some pictures yo")
		#do it
		while(t1.isAlive()):
			print("waiting for t1 thread to finish")
			t1.join(.5)

		runPhotoBooth()
		t1 = threading.Thread(target=imagemagick.generate_preview, args=[])
		#need a better timing for this
		#t1.start()
		displayRequestButtonWindow()

	if(counter2 > 10):
		print("finished 10 sequence")
		break;

	time.sleep(1)
pygame.display.quit()
sys.exit(0)
#subprocess.call("raspistill -fp -op 254 -t 3000 -o image.jpg", shell=True)










'''


#display request to user to hit buton
displayRequestButtonWindow()

#main loop
# doesn't stop running
# wait for user to press button and then take action
counter = 0
#while True:
while (counter <= 3):
	if(isButtonPressed() == False and counter < 3):
		counter = counter+1
		continue;
	else:
		#counter = 0
		counter = counter+1
		print("Button pushed, let's take some pictures yo")
		#do it
		runPhotoBooth()

	time.sleep(1)
'''