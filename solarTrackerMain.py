#!/usr/bin/python3

import serial
from base import*
from weatherData import *
from sun_position_calc import *
from region_properties import*
from image_pca import*
from servo_angle_change import *


### Initialization
#------ Start logging feature-------

#----- Set up serial connection with Uno-------              
# Turn the Serial Protocol ON
port = '/dev/ttyACM0'
baud = 9600
Serial.begin(9600);
ser = serial.Serial(port, baud, timeout = 6)

#----- Make sure WIFI is working-------

#------Connect to server-------
#------Connect to camera-------

#-----Get inital position of servos------
val_vertical=str(y_zenith[0]);
val_horizontal=str(x_azimuth[0]);

### Loop
while(1):
	### Check weather to see if can open top/raining
	getWeatherForTop()
	getForecastForTop()
	
	### Open/close top cover
	### Move servo
	ser.write(val_vertical.encode('utf-8'))
	ser.write(val_vertical.encode('utf-8'))
	time.sleep(3)
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
