#!/usr/bin/python3

import serial
import urllib
#from base import*
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
loop_value = 1
while loop_value == 1:
	print ("test 1")
	try:
		urllib.request.urlopen("http://google.com")
		loop_value=0
	except urllib.error.URLError as e:
		print(e.reason)
		f.write( "Network currently down." )
	time.sleep(5)
else:
	print( "Up and running." )
#------Connect to camera-------

#-----Get inital position of servos------

val_vertical=str(y_zenith[i]);
val_horizontal=str(x_azimuth[i]);

### Loop
while(1):
	### Check weather to see if can open top/raining
	getWeatherForTop()
	getForecastForTop()
	
	### Open/close top cover
	if 
	### Move servo
	ser.write(val_vertical.encode('utf-8'))
	ser.write(val_horizontal.encode('utf-8'))
	time.sleep(3)
	
	### Get image from camera
	
	### Find center of sun in image taken by camera
	[xC, yC, height, width]=GetCenter(img):
	
	### Check if sun in scope
	[rightPixel, leftPixel, downPixel, upPixel]=pixel_distance(height/2, width/2, xC, yC);	
	[flag1, flag2]=acceptedErrorCheck(rightPixel, leftPixel, downPixel, upPixel);
	### If not,
	if flag1 == 1 or flag2 == 1
		### Get position of servos on mirror
		[move, iChange, jChange]=SunCenteredCheck(flag1, flag2);
		### Calculate how far to move
		[move, motor_i, motor_j]=sendPosition(move, iChange, jChange);	
		### Send move to Uno
		ser.write(motor_i.encode('utf-8'))
		ser.write(motor_j.encode('utf-8'))
		time.sleep(3)
		
	### Save good image on computer
	else

### Functions

### Interrupts
#TODO: Make interrupt on time 1hr after nextAPI point when stops raining to allow top cover to open
