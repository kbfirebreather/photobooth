'''******************************************
ink_levels.py 

-script that continually checks ink levels of the printer
-Notifies users when any of the ink levels reach < 25%


******************************************'''

import re #regex dependency
import smtplib #sending email dependency
import sys
import threading
import time
import subprocess #for command line
import os
import my_globals


#variable main thread will change to TRUE if ink_levels thread is supposed to stop and exit
killThread = False

#file to get gmail credentials for sending email
email_user_password_file = "./gmail.txt"
#file to get addresses of users to be notified about low ink levels
receiver_user_file = "./inklevel_receivers.txt"

#read email user/pw file 
set_email = open(email_user_password_file, "r")

#save email user/pw into variables for mailing function
#user should be first line
gmail_user = set_email.readline().strip()
#password should be second line
gmail_pw = set_email.readline().strip()

#read notification addresses into variable
receivers = open(receiver_user_file).readlines()
#strip new line characters from list entries
receivers = map(lambda s: s.strip(), receivers)

#ink level file path/location to save ink level command into
ink_level_file_path = "/home/pi/inklevels.txt"
ink_level_file_path = "./inklevels.txt"

#variable to set when users are notified so we don't notify them every 25 seconds
#set to true when users are notified
#set back to false when ink has been replaced
notified_low_levels = False

#regex patterns for ink levels / noaccess
black = re.compile("Black:")
color = re.compile("Color:")
photo = re.compile("Black, Cyan, Magenta:")
noaccess = re.compile("Could not access")

def saveInkLevels():
	#thestr = subprocess.check_output("ink -p usb", shell=True)#os.system("ink -p usb")# > " + ink_level_file_path)
	os.system("sudo ink -p usb > " + ink_level_file_path)
	#print(thestr)
	print("done")

#function to notify/text/email/etc technicians the status of the ink levels
def notifyUsers(ink_black, ink_color, ink_photo):
	#setup message for ink levels
	msg = "Low on ink. Current Levels: \nBlack(#56): " + str(ink_black) + "%\n" + "Color(#57): " + str(ink_color) + "%\n" + "Photo(#58): " + str(ink_photo) + "%"

	#generate complete message including from/to/subject headers
	message = """From: Photobooth <noreply@photobooth.com>
	To: VIPS
	Subject: Photobooth Ink Level Notification

	"""	+ msg

	#configure smtp server settings to send the email
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.ehlo()
	server.starttls()
	server.login(gmail_user, gmail_pw)
	server.sendmail(gmail_user, receivers, message)
	server.close()
	#done notifying users
	

#function to check status of ink levels on the printer
def checkInkLevel():
	#declare this as global, otherwise can't use it
	global notified_low_levels
	#save current ink levels to a file
	saveInkLevels()
	#open saved file for readings
	f = open(ink_level_file_path, "r")
	#read entire contents into @levels
	foundInkLevels = 0
	#iterate over lines in file
	for line in f:
		#check black cartridge
		if(re.search(black, line)):
			#remove "Black:" from line
			percent = re.sub(black, "", line)
			#trim and remove %
			percent_black = percent.strip().replace("%", "")
			print("found black! " + percent_black)
			foundInkLevels += 1

		#check color cartridge
		if(re.search(color, line)):
			#remove "Color:" from line
			percent = re.sub(color, "", line)
			#trim and remove %
			percent_color = percent.strip().replace("%", "")
			print("Found color! " + percent_color)
			foundInkLevels += 1

		#check photo cartdige
		if(re.search(photo, line)):
			#remove "Black, Cyan, Magenta:" from line
			percent = re.sub(photo, "", line)
			#trim and remove %
			percent_photo = percent.strip().replace("%", "")
			print("Found photo! " + percent_photo)
			foundInkLevels += 1

		#check for usb access issues
		if(re.search(noaccess, line)):
			print("Can't access!")
			#close opened file
			f.close()
			#leave checkInkLevel() function...can't do anything yet
			#return false so when system starts it can verify it has usb access
			return False

	#if we have < 3 ink levels, then we probably didn't have access to USB and couldn't get ink levels		
	if(foundInkLevels < 3):
		#close opened file
		f.close()
		#leave function to prevent testing percentages we couldn't get
		return

	#convert percentage strings into integers for integer evaluation
	percent_black = int(percent_black)
	percent_color = int(percent_color)
	percent_photo = int(percent_photo)

	#test ink levels
	if(percent_black < 25 or percent_color < 25 or percent_photo < 25):
		#make sure they werne't notified already
		if(notified_low_levels == False):
			#set variable to indicate users have been notified
			notified_low_levels = True
			#nofity users if ink levels are lower than required amount
			notifyUsers(percent_black, percent_color, percent_photo)
	else:
		#ink levels are fine
		#reset users notified variable so users will be notified next time ink is low
		notified_low_levels = False

	#close opened file
	f.close()
	return True

#function for thread to execute constant ink level monitoring
def checkInkLevelThread():
	#iterate indefinitely
	while(True):
		#test to see if main thread notified this thread to exit
		if(killThread):
			return
		my_globals.thread_lock.acquire()
		try:
			#check ink level
			checkInkLevel()
		finally:
			#release lock
			my_globals.thread_lock.release()

		#sleep 25 seconds until checking ink levels next
		time.sleep(25)