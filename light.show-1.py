#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep
import sys
from optparse import OptionParser
import os

#relays = [3, 5, 7, 11, 13, 15, 19, 21]

porch1 = 3
porch2 = 5
shrub1 = 7
shrub2 = 11
shrub3 = 13
shrub4 = 15
tree = 19
shrub5 = 21

relays = [porch1, porch2, shrub1, shrub2, shrub3, shrub4, shrub5]

blink_delay = .2
grow_delay = .2

def_loop = 3
wait_count = 0

parser = OptionParser()
parser.add_option("--off", action="store_true", dest="lightsOff")
parser.add_option("--on", action="store_true", dest="lightsOn")

(opts, args) = parser.parse_args()

def setup():

#    GPIO.setmode(GPIO.BCM)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(relays, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(tree, GPIO.OUT, initial=GPIO.HIGH)

# Base function to turn relay on, pass it board gpio pin number
def relay_on(relay):
    #print "Relay on " + str(relay)
    GPIO.output(relay, GPIO.LOW)
    
# Base function to turn relay off, pass it board gpio pin number
def relay_off(relay):
    #print "Relay off " + str(relay)
    GPIO.output(relay, GPIO.HIGH)

def all_on():
    for r in relays:
        relay_on(r)

def all_off():
    for r in relays:
        relay_off(r)

def all_blink():
    msgOut("Blink all...")
    all_off()
    for relay in relays:
        relay_on(relay)
    sleep(blink_delay)
    for relay in relays:
        relay_off(relay)
    sleep(blink_delay)
        
def blink_on(relay):
    relay_on(relay)
    sleep(blink_delay)
    relay_off(relay)
    
def blink_off(relay):
    relay_off(relay)
    sleep(blink_delay)
    relay_on(relay)
        
def grow_on():
    for relay in relays:
        #print "LED on " + str(relay)
        relay_on(relay)
        sleep(grow_delay)

def grow_off():
    for relay in relays:
        #print "LED off " + str(relay)
        relay_off(relay)
        sleep(grow_delay)
        
def grow_on_reverse():
    for relay in relays[::-1]:
        #print "LED on " + str(relay)
        relay_on(relay)
        sleep(grow_delay)
               
def grow_off_reverse():
    for relay in relays[::-1]:
        #print "LED off " + str(relay)
        relay_off(relay)
        sleep(grow_delay)
        
def msgOut(string):
    print "****************************************************"
    print "*                                                  *"
    print "* " + str(string)
    print "*                                                  *"
    print "****************************************************"
   
setup()

#sleep(2)

if( opts.lightsOn ):
    all_on()
    exit(0)

if( opts.lightsOff ):
    all_off()
    exit(0)
  
relay_on(tree)

while(1):

    if os.path.isfile("/etc/lights.on"):

        msgOut("Start of sequence blink all")
        for x in range(0, def_loop):
            all_blink()
        
        msgOut("Loop through turn porch on...")
        for x in range(0, def_loop):
            relay_on(porch1)
            relay_on(porch2)
            sleep(.1)
            relay_off(porch1)
            relay_off(porch2)
            sleep(.1)
        
        msgOut("Blink tree off and on...")
        blink_off(tree)
    
        msgOut("Loop through turn all on...")
        for x in range(0, def_loop):
            all_on()
            sleep(.1)
            all_off()
            sleep(.1)
     
        #Chase
        msgOut("Chase...")
        for x in range(0, def_loop):
            for x in range(0, len(relays)):
                blink_on(relays[x])
                sleep(.1)
       
        msgOut("Blink tree off and on...")
        blink_off(tree)
 
        msgOut("Loop through grow all on...")
        for x in range(0, def_loop):
            grow_on()
            sleep(.2)
            grow_off()
            sleep(.1)
        
        msgOut("Blink tree off and on...")
        blink_off(tree)
        
        msgOut("Loop through turn all on 1...")
        for r in relays:
            #print "LED on " + str(r)
            relay_on(r)
            sleep(.2)
        
        msgOut("Loop through turn all off...")    
        for r in relays:
            relay_off(r)
            sleep(.1)
    
        msgOut("Loop through turn all on 2...")
        for x in range(0, def_loop):
            grow_on_reverse()
            sleep(.1)
            
            grow_off_reverse()
            sleep(.25)
        
        msgOut("Loop through turn all on 3...")  
        for x in range(0, def_loop):
            all_on()
            sleep(.1)
            all_off()
            sleep(.5)
    else:

        if wait_count == 0:
            msgOut("Holding to turn lights back on...")
            all_off()
            relay_off(tree)
            
        if wait_count >= 5:
            wait_count = 1
        
        wait_count += 1    
        sleep(60)
        
        

