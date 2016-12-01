#!/usr/bin/python3
import os               																				
import math
import cmath
import sched  
import serial
import urllib
import time
import datetime

from weatherData import *
from sun_position_calc import *
#from region_properties import*
from servo_position_change import *
from scheduler import*


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

#-----Open or Close Protection Unit------
def ProtectionUnitCover(ser):
	### Get Weather codes
	topWeatherCodes=getWeatherForTop();
	WeatherStatus= topWeatherCodes['badWeatherNow']
	CoverStatus= topWeatherCodes['topCurrentStatus']

	if WeatherStatus == 1 and CoverStatus == 1 : # Cover is open and weather is bad
		### Close Protection Unit 
		CoverStatus=0;
		motor_pro= str(900)
		ser.write(motor_pro.encode('utf-8'))
		
	if WeatherStatus == 0 and CoverStatus == 0: # Cover is closed and weather is good
		### Open protection Unit 
		CoverStatus=1;
		motor_pro= str(100)
		ser.write(motor_pro.encode('utf-8'))
		
	return(CoverStatus)
	
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
	
	Hour= h[3];
	Minute=h[4];
	return (Hour, Minute)
	
#----Getting SunPosition every hour 8:30AM-4:30PM--------
def HourlySunPosition(ser):
	[motor_azimuth,motor_zenith]=_hourly_position_();
	#[Hour,Minute]=getTime();
	#[x_azimuth,y_zenith]=_hourly_position_();
	#if  Hour == 8: # Time is 8:30AM
		#val_vertical=str(y_zenith[0]);	
		#val_horizontal=str(x_azimuth[0]);	
	#elif  Hour == 9: # Time is 9:30AM
		#val_vertical=str(y_zenith[1]);	
		#val_horizontal=str(x_azimuth[1]);
	#elif  Hour == 10: # Time is 10:30AM
		#val_vertical=str(y_zenith[2]);	
		#val_horizontal=str(x_azimuth[2]);
	#elif Hour == 11: # Time is 11:30AM
		#val_vertical=str(y_zenith[3]);	
		#val_horizontal=str(x_azimuth[3]);
	#elif Hour == 12: # Time is 12:30PM
		#val_vertical=str(y_zenith[4]);	
		#val_horizontal=str(x_azimuth[4]);
	#elif Hour == 13:# Time is 1:30PM
		#val_vertical=str(y_zenith[5]);	
		#val_horizontal=str(x_azimuth[5]);
	#elif Hour == 14:# Time is 2:30PM
		#val_vertical=str(y_zenith[6]);	
		#val_horizontal=str(x_azimuth[6]);
	#elif Hour == 15: # Time is 3:30PM
		#val_vertical=str(y_zenith[7]);	
		#val_horizontal=str(x_azimuth[7]);
	#elif Hour == 16: # Time is 4:30PM
		#val_vertical=str(y_zenith[8]);	
		#val_horizontal=str(x_azimuth[8]);
	
	val_vertical=str(y_zenith[0]);	
	val_horizontal=str(x_azimuth[0]);	
	### Move Tracker	
	[old_i, old_j]= MotorMovementTracker(ser,val_vertical,val_horizontal);
	return(old_i, old_j)
	
		
#-----Moving Solar Tracker------
def	 MotorMovementTracker( ser,val_vertical,val_horizontal):
	### Move Tracker
	import time
	motor_ver='v';
	motor_hor='h';
	
	ser.write(motor_ver.encode('utf-8'))
	time.sleep(1)
	[ver_pos]=ser.write(val_vertical.encode('utf-8'))
	time.sleep(2)
	ser.write(motor_hor.encode('utf-8'))
	time.sleep(1)
	[hor_pos]=ser.write(val_horizontal.encode('utf-8'))
	time.sleep(2)

	[var, old_i]=str.split(ver_pos)
	[var, old_j]=str.split(hor_pos)
	
	return (int(old_i), int(old_j))

#-----Check to see if sun is centered in first image-----
def CheckSunCentered(ser,old_i, old_j):
	### Get image from camera
	[img]=cameraConnetion()
	
	### Find center of sun in image using image processing 
	#[xC, yC, height, width]=GetCenter(img);
	#xC=234
	#yC=560
	#height=960
	#width=1200
	
	### Check if sun is in scope
	[rightPixel, leftPixel, downPixel, upPixel]=pixel_distance(height/2, width/2, xC, yC);
	move=acceptedErrorCheck(rightPixel, leftPixel, downPixel, upPixel);
	
	### Call function to see if image is centered
	AdjustTracker(old_i,old_jmove,img,height, width, rightPixel, leftPixel, downPixel, upPixel,ser);

#---- Adjusts Tracker until sun is centered in image----
def AdjustTracker(old_i,old_j,move,img,height, width, rightPixel, leftPixel, downPixel, upPixel, ser):
	while (move == 1):
		### Get position of servos on mirror
		[iChange, jChange]=SunCenteredCheck(height, width, rightPixel, leftPixel, downPixel, upPixel);
		
		### Get old angle from servo motor
		
		### Calculate how far to move
		[motor_i, motor_j]=sendPosition(move, iChange, jChange,old_i, old_j);	
		
		### Send move to Uno
		import time
		motor_ver='v';
		motor_hor='h';
		motor_feedback='p';
		
		ser.write(motor_ver.encode('utf-8'))# specifing vertical motor
		time.sleep(1)
		ser.write(motor_i.encode('utf-8'))# sending vertical position
		time.sleep(2)
		[old_i]=ser.write(motor_feedback.encode('utf-8'))
		time.sleep(1)
		ser.write(motor_hor.encode('utf-8'))# specifing horizontal motor
		time.sleep(1)
		ser.write(motor_j.encode('utf-8'))# sending horizontal posistion
		time.sleep(2)
		[old_j]=ser.write(motor_feedback.encode('utf-8'))
		
		[var, old_i]=str.split(old_i);
		[var, old_j]=str.split(old_j);
		
		old_i=int(old_i);
		old_j=int(old_j);
		### Get image from camera
		[img]=cameraConnetion();
		
		### Find center of sun in image using image processing 
		[xC, yC, height, width]=GetCenter(img);
		#xC=234
		#yC=560
		#height=960
		#width=1200
		
		### Check if sun is in scope
		[rightPixel, leftPixel, downPixel, upPixel]=pixel_distance(height/2, width/2, xC, yC);
		move=acceptedErrorCheck(rightPixel, leftPixel, downPixel, upPixel);
				
	### Save good image on computer
	img.save(img)

### Function Calls
[ser]=serialConnectionCheck();
wifiConnectionCheck();

__init__(self);
#[CoverStatus]=ProtectionUnitCover();
#if CoverStatus == 1:
	#HourlySunPosition(ser,);
	#CheckSunCentered(ser,old_i, old_j);
	

### Interrupts
#TODO: Make interrupt on time 1hr after nextAPI point when stops raining to allow top cover to open
