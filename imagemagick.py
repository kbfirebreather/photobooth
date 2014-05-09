'''******************************************
imagemagick.py 

-python script to handle all imagemagick commands

-resizes/crops pictures
-creates final picture to be printed


******************************************'''

import os
import random
import threading
import time

import my_globals

#root directory for photos
#dirPrefix = "/home/pi/python/photos/"

#cmd line string
def cmd_line(string):
	print("started: " + string)
	start = time.time()
	os.system(string)
	end = time.time() - start
	print("ended in " + str(end) + " seconds: " + string)


#function to make super preview block
def generate_preview():
	#read files in 
	#verify enough files for this to happen
	os.chdir(my_globals.PBOOTH_THUMBS)
	#num rows for grid
	rows = 8
	#num cols for grid
	cols = 9

	montage = "montage -geometry +1+1 -tile " + str(cols) + "x" + str(rows) + " -background '#0000FF' -alpha Opaque "

	shuffled_files = []
	#iterate through files and save into array
	for files in os.listdir("."):
		shuffled_files.append(files)
	#shuffle array for random order
	random.shuffle(shuffled_files)
	counter = 0
	#iterate through array
	for x in range(0, len(shuffled_files)):
		#concatentate montage command for new file
		montage = montage + my_globals.PBOOTH_THUMBS + shuffled_files[x] + " -resize 107x80 "
		counter += 1
		#check to see if we reached our rowxcol limit
		if(counter >= rows*cols):
			break; #break out of loop if we want to stay within rowxcol constraint

	#complete montage command for output file
	montage = montage + my_globals.PBOOTH_BOTTOM + "big_preview.jpg"
	#print(montage)
	#verify there was files before executing command
	if(len(shuffled_files) > 0):
		os.system(montage) #execute command

	print("done making preview")



#function to turns 6 images into 4x6 print off
def montage(images, thumbs, threads, id = ""):
	print threads
	print thumbs
	print images


	num_images = 4
	#verify the supplied images array matches expected @num_images
	if(len(images) != num_images):
		return False

	#verify num thumbs
	if(len(images) != len(thumbs)):
		return False

	#wait for threads to finish
	start_threads_time = time.time()
	for x in range(0, len(threads)):
		threads[x].join()

	end_threads_time = time.time()

	#verify supplied files exist
	for y in range(0, num_images):
		if(os.path.isfile(my_globals.PBOOTH_DIR + images[y]) == False):
			print("No image[y]")
			return False #return false of any of the 'images' doesn't exist
		if(os.path.isfile(my_globals.PBOOTH_THUMBS + thumbs[y]) == False):
			print("no thumbnail")
			return False #thumbnail file doesn't exist

	
	#montage command to stitch all together @300dpi
	#montage = "montage -geometry +2+2 -tile 2x3 -density 300 -background '#CC00CC' -alpha Opaque "
	montage = "montage -geometry +1+1 -tile 2x2 -density 300 -background '#0000FF' -alpha Opaque "
	#generate montage command with thumbnail images
	for x in range(0, len(thumbs)):
		montage = montage  + " " + my_globals.PBOOTH_THUMBS + thumbs[x] + " -crop 598x598+101+0 "

	#print(montage)
	#complete montage command to set output file 
	# should be montage -geometry +0+0 -tile 2x3 -density 300 img1 img2 img3 img4 img5 img6 out.jpg
	montage = montage + my_globals.PBOOTH_SETS + "complete_" + id + ".jpg "

	print("\n\nMontaging")
	cmd_line(montage)
	'''
	os.system(montage)
	print("dont montaging")
	'''

	#bottom of the complete file
	bottom_file = my_globals.PBOOTH_BOTTOM + "banner.jpg"
	#stitch together the 2x3 and the bottom_file
	montage2 = "montage " + my_globals.PBOOTH_SETS + "complete_" + id + ".jpg " + bottom_file + " -tile 1x2 -geometry +0+0 " + my_globals.PBOOTH_SETS + "complete_" + id + ".jpg "
	#make final photo booth picture product to be printed
	print("\n\nmontag2")
	cmd_line(montage2)
	'''
	os.system(montage2)
	print("done montag 2")
	'''

	return end_threads_time - start_threads_time