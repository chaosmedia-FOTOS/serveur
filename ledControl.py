#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import thread

sleepingTime = 0.05
tabPin = []

"""
	Functions
"""

def print_time(pin):
	first = True

	while (tabPin[pin][2] > 0 and tabPin[pin][4] < tabPin[pin][1]) or (tabPin[pin][2] < 0 and tabPin[pin][4] > tabPin[pin][1]):
		if not first:
			time.sleep(sleepingTime)
		else:
			first = False

		tabPin[pin][4] += tabPin[pin][2]

		if tabPin[pin][4] > 100 :
			tabPin[pin][4] = 100
		elif tabPin[pin][4] < 0 :
			tabPin[pin][4] = 0

		tabPin[pin][0].ChangeDutyCycle(tabPin[pin][4])
			
	tabPin[pin][3] = False

def fadeTo(unePin, value, temps):
	
	value = round(value / 2.55, 0)

	for pin in range(len(tabPin), unePin+1):
		tabPin.append([0 for i in range(6)])
		tabPin[pin][1] = 0					#Valeur (Goal)
		tabPin[pin][2] = 0					#Step
		tabPin[pin][3] = False				#On/Off
		tabPin[pin][4] = 0					#Valeur actuel
		tabPin[pin][5] = False				#Setuped

	#Setup la pin si elle n'est pas encore cree
	if not tabPin[unePin][5]:
		GPIO.setup(unePin, GPIO.OUT)
		tabPin[unePin][0] = GPIO.PWM(unePin, 150)	#Porte/Frequence
		tabPin[unePin][0].start(0)
		tabPin[unePin][5] = True


	tabPin[unePin][1] = value

	if temps == 0 or temps == 1:
		tabPin[unePin][2] = value - tabPin[pin][4]
	else:
		dif = value- tabPin[unePin][4]
		step = dif/(float(temps)/1000) * sleepingTime

		tabPin[unePin][2] = step
	
	if(tabPin[unePin][3] == False):
		tabPin[unePin][3] = True
		thread.start_new_thread( print_time, (unePin, ))

"""
	Main
"""
try:
	GPIO.setmode(GPIO.BCM)

	#test
	while True:
		fadeTo(23,255,2000)	
		time.sleep(1)
		fadeTo(18,125,1000)
		time.sleep(1)
		fadeTo(22,200,3000)
		time.sleep(1)
		fadeTo(23,0,2000)
		time.sleep(1)
		fadeTo(18,0,2000)
		time.sleep(1)
		fadeTo(22,0,2000)
		time.sleep(1.5)

finally:
	GPIO.cleanup()
	pass