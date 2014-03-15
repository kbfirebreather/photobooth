import RPi.GPIO as GPIO
import os
import sys
import time
import threading



'''******************************************
gpio_handler.py 

-Handles all GPIO Events

-Checks for when button is pressed so photobooth can work it's magic

-Handles countdown timer through GPIO pins


******************************************'''




def exit():
	GPIO.cleanup()

#set mode for GPIO
#BCM are the good numbers
#BOARD are the stupid numbers
GPIO.setmode(GPIO.BCM)

#configure gpio pins we'll be using
#initialize to LOW
GPIO.setup(25, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)

#for button press
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)




#detect if button is pressed
#return TRUE if pressed
#return FALSE if not pressed
def isButtonPressed():
	#if pressed, return true
	#else
	#return false
	print("Waiting for falling edge")
	GPIO.wait_for_edge(17, GPIO.FALLING)
	print("edge fell")
	return True
	#return True
	#while True:
		#print(GPIO.input(17))
	#return GPIO.input(17) == 0

#quick function for setting GPIO state
def setGPIO(gpio, state):
	GPIO.output(gpio, state)

#while(True):
def displayCountdown():
	#wait 0.6 seconds before displaying countdown as that's how long it takes to prep camera
	time.sleep(.65)
	#lets cound down from 3,2,1....
	#let's display 3!
	#first set all LOW
	setGPIO(25, False)
	setGPIO(24, False)
	setGPIO(23, False)
	setGPIO(22, False)

	#display 3!
	#print("display 3")
	setGPIO(25, True)
	setGPIO(24, True)
	setGPIO(22, True)

	#wait 1 second before displaying next number!
	time.sleep(1)

	#display 2!
	#remove segment for #3 that's not used for #2
	setGPIO(24, False)
	#display segment used for #2
	#print("display 2")
	#setGPIO(25, True)
	setGPIO(23, True)

	#wait 1 second before displaying next number!
	time.sleep(1)

	#display 1!
	#remove segments for #2 that's not used in #1
	setGPIO(23, False)
	setGPIO(22, False)

	#display segment used for #1!
	#print("display 1")
	setGPIO(24, True)

	#wait 1 second!
	time.sleep(1)

	#remove all led displays
	setGPIO(24, False)
	setGPIO(25, False)

	'''
	print("Setting GPIO 25 output HI")
	setGPIO(25, True)
	time.sleep(3)
	print("Setting GPIO 25 output LO")
	setGPIO(25, False)
	time.sleep(3)
	'''

def countdownThread():
	t1 = threading.Thread(target=displayCountdown, args=[])
	t1.start()

'''
print("executing thread")

while(True):
	print("looping out of thread...")
	time.sleep(0.1)
'''