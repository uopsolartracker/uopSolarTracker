#!/usr/bin/python3

import weatherData

### Initialization
# Start logging feature
# Set up serial connection with Uno
# Make sure WIFI is working
# Connect to server
# Connect to camera
# Get inital position of servos?

### Loop
while(1):
	### Check weather to see if can open top/raining
	### Open/close top cover
	### Check if sun in scope
		### If not,
			### Detech edges
			### Get position of servos on mirror
			### Calculate how far to move
			### Send move to Uno
	### Send good image to server

### Functions

### Interrupts
#TODO: Make interrupt on time 1hr after nextAPI point when stops raining to allow top cover to open
