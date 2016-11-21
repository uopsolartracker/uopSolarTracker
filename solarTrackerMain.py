#!/usr/bin/python3
import os               																				
import math
import cmath
import sched  
import serial
import urllib
import time
import datetime
import json

from weatherData import *
from sun_position_calc import *
from region_properties import*
import servo_position_change 


### Initialization
#------ Start logging feature-------

#----- Set up serial connection with Uno-------  
def serialConnectionCheck():            
	### Turn the Serial Protocol ON
	port = '/dev/ttyACM0'
	baud = 9600
	ser = serial.Serial(port, baud, timeout = 6)
	return ser

#----- Make sure WIFI is working-------
def wifiConnectionCheck():
	### Test wifi connection
	print ("test 1")
	loop_value = 1
	while loop_value == 1:
		print ("test 2")
		try:
			urllib.request.urlopen("http://google.com")
			loop_value=0
		except urllib.error.URLError as e:
			print(e.reason)
			f.write( "Network currently down." )
		import time
		time.sleep(5)
	else:
		print( "Up and running." )

#------Connect to camera-------
def cameraConnetion():

	return(img) 

#-----Check weather to see if can open/close top-------
def WeatherCheck():
	### Check weather codes for current weather and cover status
	topWeatherCodes=getWeatherForTop();
	WeatherStatus= topWeatherCodes['badWeatherNow']
	CoverStatus= topWeatherCodes['topCurrentStatus']
	return (WeatherStatus, CoverStatus) 

#-----Open or Close Protection Unit------
def ProtectionUnitCover(WeatherStatus, CoverStatus):
	if WeatherStatus == 1 and CoverStatus == 1 : # Cover is open and weather is bad
		### Close Protection Unit
		topWeatherCodes['topCurrentStatus']=0;
		
		### Check weather staus every 10 minutes until good weather
		while(WeatherStatus == 1):
			topWeatherCodes=getWeatherForTop();
			WeatherStatus = topWeatherCodes['badWeatherNow'];
			import time
			time.sleep(600)
		### Once weather status is good open protection unit
		if WeatherStatus == 0:
			### Open protection Unit 
			topWeatherCodes['topCurrentStatus']=1;
			### Check future weather status
			topFutureWeather=getForecastForTop()
			weather8AM=topFutureWeather['WeatherEightAM']
			weather11AM=topFutureWeather['WeatherElevenAM']
			weather2PM=topFutureWeather['WeatherTwoAM']
			weather5PM=topFutureWeather['WeatherFiveAM']

	elif WeatherStatus == 1 and CoverStatus == 0 :# Cover is closed and weather is bad
		### Check weather staus every 10 minutes until good weather
		while(WeatherStatus == 1):
			topWeatherCodes=getWeatherForTop();
			WeatherStatus = topWeatherCodes['badWeatherNow'];
			import time
			time.sleep(600)
		### Once weather status is good open protection unit
		if WeatherStatus == 0:
			### Open protection Unit 
			topWeatherCodes['topCurrentStatus']=1;
			### Check future weather status
			topFutureWeather=getForecastForTop()
			weather8AM=topFutureWeather['WeatherEightAM']
			weather11AM=topFutureWeather['WeatherElevenAM']
			weather2PM=topFutureWeather['WeatherTwoAM']
			weather5PM=topFutureWeather['WeatherFiveAM']

	elif WeatherStatus == 0 and CoverStatus == 0: # Cover is closed and weather is good
		### Open protection Unit 
		topWeatherCodes['topCurrentStatus']=1;
		
		### Check future weather status
		topFutureWeather=getForecastForTop()
		weather8AM=topFutureWeather['WeatherEightAM']
		weather11AM=topFutureWeather['WeatherElevenAM']
		weather2PM=topFutureWeather['WeatherTwoAM']
		weather5PM=topFutureWeather['WeatherFiveAM']
	
	else: # Cover is open and weather is good
		### Check future weather status
		topFutureWeather=getForecastForTop()
		weather8AM=topFutureWeather['WeatherEightAM']
		weather11AM=topFutureWeather['WeatherElevenAM']
		weather2PM=topFutureWeather['WeatherTwoAM']
		weather5PM=topFutureWeather['WeatherFiveAM']
	return(weather8AM,weather11AM,weather2PM, weather5PM)
	
#----This will be replaced by the schedular-------
def getTime():
	import time
	import datetime
	
	# get timestamp 
	timeStamp= time.time();

	# convert timestamp to humanreadable form
	humanReadable_TS= datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d-%H-%M-%S');

	# parse human readable to create variables for year, month, day, etc.
	h = humanReadable_TS.split("-");
	# Hour
	
	Hour= h[3]
	return Hour
	
#----Getting SunPosition every hour 8:30AM-4:30PM--------
def currentSunPosition(Hour):
	if  Hour == 8 # Time is 8:30AM
		val_vertical=str(y_zenith[0]);	
		val_horizontal=str(x_azimuth[0]);	
	elif  Hour == 9 # Time is 9:30AM
		val_vertical=str(y_zenith[1]);	
		val_horizontal=str(x_azimuth[1]);
	elif  Hour == 10 # Time is 10:30AM
		val_vertical=str(y_zenith[2]);	
		val_horizontal=str(x_azimuth[2]);
	elif Hour == 11 # Time is 11:30AM
		val_vertical=str(y_zenith[3]);	
		val_horizontal=str(x_azimuth[3]);
	elif Hour == 12 # Time is 12:30PM
		val_vertical=str(y_zenith[4]);	
		val_horizontal=str(x_azimuth[4]);
	elif Hour == 13 # Time is 1:30PM
		val_vertical=str(y_zenith[5]);	
		val_horizontal=str(x_azimuth[5]);
	elif Hour == 14 # Time is 2:30PM
		val_vertical=str(y_zenith[6]);	
		val_horizontal=str(x_azimuth[6]);
	elif Hour == 15 # Time is 3:30PM
		val_vertical=str(y_zenith[7]);	
		val_horizontal=str(x_azimuth[7]);
	elif Hour == 16 # Time is 4:30PM
		val_vertical=str(y_zenith[8]);	
		val_horizontal=str(x_azimuth[8]);
	return 	(val_vertical, val_horizontal)
		
#-----Moving Solar Tracker------
def	 MotorMovementTracker(weather8AM,weather11AM,weather2PM, weather5PM, ser, val_vertical,val_horizontal):
	### Move Tracker
	import time
	ser.write(val_vertical.encode('utf-8'))
	time.sleep(3)
	ser.write(val_horizontal.encode('utf-8'))
	time.sleep(3)

#-----Check to see if sun is centered in first image-----
def CheckSunCentered():
	### Get image from camera
	
	### Find center of sun in image using image processing 
	[xC, yC, height, width]=GetCenter(img):
	#xC=234
	#yC=560
	#height=960
	#width=1200
	### Check if sun is in scope
	[rightPixel, leftPixel, downPixel, upPixel]=pixel_distance(height/2, width/2, xC, yC);
	move=acceptedErrorCheck(rightPixel, leftPixel, downPixel, upPixel);
	return (move,img,height, width, rightPixel, leftPixel, downPixel, upPixel)

#---- Adjusts Tracker until sun is centered in image----
def AdjustTracker(move,img,height, width, rightPixel, leftPixel, downPixel, upPixel):
	while (move == 1):
		### Get position of servos on mirror
		[iChange, jChange]=SunCenteredCheck(height, width, rightPixel, leftPixel, downPixel, upPixel);
		### Get old angle from servo motor
		
		### Calculate how far to move
		[motor_i, motor_j]=sendPosition(move, iChange, jChange,old_i, old_j);	
		### Send move to Uno
		ser.write(motor_i.encode('utf-8'))
		time.sleep(3)
		ser.write(motor_j.encode('utf-8'))
		time.sleep(3)
		
		### Get image from camera
	
		### Find center of sun in image using image processing 
		[xC, yC, height, width]=GetCenter(img):
		#xC=234
		#yC=560
		#height=960
		#width=1200
		
		### Check if sun is in scope
		[rightPixel, leftPixel, downPixel, upPixel]=pixel_distance(height/2, width/2, xC, yC);
		move=acceptedErrorCheck(rightPixel, leftPixel, downPixel, upPixel);
				
	### Save good image on computer
	img.save('/absolute/path/to/myphoto.jpg', 'JPEG')

### Function Calls
[ser]serialConnectionCheck();
wifiConnectionCheck();
[WeatherStatus, CoverStatus]=WeatherCheck();
[weather8AM,weather11AM,weather2PM, weather5PM]=ProtectionUnitCover(WeatherStatus, CoverStatus);
[Hour]=getTime();
[val_vertical, val_horizontal]=currentSunPosition(Hour);
MotorMovementTracker(weather8AM,weather11AM,weather2PM, weather5PM, ser, val_vertical,val_horizontal)
[move,img,height, width, rightPixel, leftPixel, downPixel, upPixel]=CheckSunCentered()
AdjustTracker(move,img,height, width, rightPixel, leftPixel, downPixel, upPixel)
### Interrupts
#TODO: Make interrupt on time 1hr after nextAPI point when stops raining to allow top cover to open
