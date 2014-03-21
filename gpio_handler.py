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




#detect if button is pressed
#return TRUE if pressed
#return FALSE if not pressed
def isButtonPressed():
	#wait for falling edge on GPIO 
	#print("Waiting for falling edge")
	#GPIO.wait_for_edge(GPIO_BTN, GPIO.FALLING)
	#print("Falling edge detected, returning true")
	try:
		GPIO.wait_for_edge(GPIO_BTN, GPIO.FALLING)
		print('falling detected')
		return True
	except KeyboardInterrupt:
		GPIO.cleanup()
	GPIO.cleanup()
	#try failed
	return False

	return GPIO.input(GPIO_BTN) == False
	return True

#quick function for setting GPIO state
def setGPIO(gpio, state):
	GPIO.output(gpio, state)

#function to display countdown to LED
def displayCountdown():
	#wait 0.6 seconds before displaying countdown as that's how long it takes to prep camera
	time.sleep(.65)
	#lets cound down from 3,2,1....
	#let's display 3!
	#first set all LOW
	setGPIO(GPIO_3_2_1, False)
	setGPIO(GPIO_3_2, False)
	setGPIO(GPIO_3_1, False)
	setGPIO(GPIO_2, False)

	#display 3!
	#print("display 3")
	GPIO.output(GPIO_3_2_1, True)
	GPIO.output(GPIO_3_2, True)
	GPIO.output(GPIO_3_1, True)

	#wait 1 second before displaying next number!
	time.sleep(1)

	#display 2!
	#remove segment for #3 that's not used for #2
	GPIO.output(GPIO_3_1, False)
	#display segment used for #2
	#print("display 2")
	#setGPIO(25, True)
	GPIO.output(GPIO_2, True)

	#wait 1 second before displaying next number!
	time.sleep(1)

	#display 1!
	#remove segments for #2 that's not used in #1
	GPIO.output(GPIO_3_2, False)
	GPIO.output(GPIO_2, False)

	#display segment used for #1!
	#print("display 1")
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
