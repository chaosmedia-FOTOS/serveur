#!/usr/bin/python

import Adafruit_BBIO.PWM as PWM

import time
import thread

sleepingTime = 0.05
tabPin = {}

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

		PWM.ChangeDutyCycle(tabPin[pin][0], tabPin[pin][4])
			
	tabPin[pin][3] = False

def fadeTo(unePin, value, temps):
	
	value = round(value / 2.55, 0)
	if not unePin in tabPin:
		tabPin[unePin]    = [0 for i in range(6)]

		tabPin[unePin][0] = unePin		#Pin

		tabPin[unePin][1] = 0			#Valeur (Goal)
		tabPin[unePin][2] = 0			#Step
		tabPin[unePin][3] = False		#On/Off
		tabPin[unePin][4] = 0			#Valeur actuel

		PWM.start(unePin, 150)			#Porte/Frequence

	tabPin[unePin][1] = value

	if temps == 0 or temps == 1:
		tabPin[unePin][2] = value - tabPin[unePin][4]
	else:
		dif = value- tabPin[unePin][4]
		step = dif/(float(temps)/1000) * sleepingTime

		tabPin[unePin][2] = step
	
	if(tabPin[unePin][3] == False):
		tabPin[unePin][3] = True
		thread.start_new_thread( print_time, (unePin, ))
