#!/usr/bin/env python
'''
**********************************************************************
* Filename 		: 8_channel_relay.py
* Description 	: a sample script for 8-Channel High trigger Relay 
* Author 		: Cavon
* E-mail 		: service@sunfounder.com
* Website 		: www.sunfounder.com
* Update 		: Cavon    2016-08-04
* Detail		: New file
**********************************************************************
'''
import RPi.GPIO as GPIO
from time import sleep

Relay_channel = [17, 18]

def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(Relay_channel, GPIO.OUT, initial=GPIO.LOW)
	print "|=====================================================|"
	print "|         8-Channel High trigger Relay Sample         |"
	print "|-----------------------------------------------------|"
	print "|                                                     |"
	print "|          Turn 8 channels on off in orders           |"
	print "|                                                     |"
	print "|                    17 ===> IN4                      |"
	print "|                    18 ===> IN5                      |"
	print "|                                                     |"
	print "|                                           SunFounder|"
	print "|=====================================================|"

def main():
	while True:
		for i in range(0, len(Relay_channel)):
			print '...Relay channel %d on' % i+1
			GPIO.output(Relay_channel[i], GPIO.HIGH)
			sleep(0.5)
			print '...Relay channel %d off' % i+1
			GPIO.output(Relay_channel[i], GPIO.LOW)
			sleep(0.5)

def destroy():
	GPIO.output(Relay_channel, GPIO.LOW)
	GPIO.cleanup()

if __name__ == '__main__':
	setup()
	try:
		main()
	except KeyboardInterrupt:
		destroy()

