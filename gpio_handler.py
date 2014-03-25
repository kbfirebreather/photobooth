'''******************************************
gpio_handler.py 

-Handles all GPIO Events

-Checks for when button is pressed so photobooth can work it's magic

-Handles countdown timer through GPIO pins


******************************************'''

import RPi.GPIO as GPIO
import os
import sys
import time
import threading
import my_globals


#when closing program, cleanup gpio first
def exit():
	GPIO.cleanup()

#set mode for GPIO
#BCM are the good numbers
#BOARD are the stupid numbers
GPIO.setmode(GPIO.BCM)

#pins used to display 3,2,1
GPIO_3_2_1 = 25
GPIO_3_2 = 2
GPIO_3_1 = 4
GPIO_2 = 3

#pin used for button detection
GPIO_BTN = 17

#configure gpio pins we'll be using
#initialize to LOW
GPIO.setup(GPIO_3_2_1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(GPIO_3_2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(GPIO_3_1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(GPIO_2, GPIO.OUT, initial=GPIO.LOW)

#for button press
GPIO.setup(GPIO_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#get current time in millis
#used for debouncing
def getMillis():
	return int(round(time.time() * 1000))

debounce_time = 20 #time in ms to debounce for
#function to verify GPIO button is actually pressed and not a false positive
def checkDebounce():
	#current ms
	ms_now = getMillis()
	#loop until we reach target debounce_time
	while((getMillis() - ms_now) < debounce_time):
		#if button goes back high, then this was no good
		if(GPIO.input(GPIO_BTN)):
			print("debounce detected")
			#return false to indicate failure
			return False
	#return true to indicate valid button press
	print("Seems like valid button press")
	return True


#detect if button is pressed
#return TRUE if pressed
#return FALSE if not pressed
def isButtonPressed():
	buttonPressed = False
	#qcquire lock
	my_globals.thread_lock.acquire()
	try:
		#wait for falling edge on GPIO 
		GPIO.wait_for_edge(GPIO_BTN, GPIO.FALLING)
		print('Falling detected')
		#validate button press 
		buttonPressed = checkDebounce()
	finally:
		my_globals.thread_lock.release()

	#return state of button press
	#false if not pressed / debounced detected
	#true if legitimate button press
	return buttonPressed

#quick function for setting GPIO output state
def setGPIO(gpio, state):
	GPIO.output(gpio, state)

#function to display countdown to LED
def displayCountdown():
	#wait 0.7 seconds before displaying countdown as that's how long it takes to prep camera
	time.sleep(.70)
	#lets cound down from 3,2,1....
	#let's display 3!
	#first set all LOW
	setGPIO(GPIO_3_2_1, False)
	setGPIO(GPIO_3_2, False)
	setGPIO(GPIO_3_1, False)
	setGPIO(GPIO_2, False)

	#display 3!
	GPIO.output(GPIO_3_2_1, True)
	GPIO.output(GPIO_3_2, True)
	GPIO.output(GPIO_3_1, True)

	#wait 1 second before displaying next number!
	time.sleep(1)

	#display 2!
	#remove segment for #3 that's not used for #2
	GPIO.output(GPIO_3_1, False)
	#display segment used for #2
	GPIO.output(GPIO_2, True)

	#wait 1 second before displaying next number!
	time.sleep(1)

	#display 1!
	#remove segments for #2 that's not used in #1
	GPIO.output(GPIO_3_2, False)
	GPIO.output(GPIO_2, False)

	#display segment used for #1!
	GPIO.output(GPIO_3_1, True)

	#wait 1 second!
	time.sleep(1)

	#remove remaining led displays
	GPIO.output(GPIO_3_1, False)
	GPIO.output(GPIO_3_2_1, False)

#function called from booth.py to execute countdown in a thread
def countdownThread():
	#create thread for displayCountdown
	t1 = threading.Thread(target=displayCountdown, args=[])
	#execute thread
	t1.start()
