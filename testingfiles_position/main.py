#!/usr/bin/python3

import os               																				
import math
import cmath
import sched  
import serial
import urllib
import time
import datetime
import cv2

from weatherData import *
from sun_position_calc import *
from servo_position_change import *
#from scheduler import*
from region_properties import region_properties

def cameraConnetion():
	img = cv2.imread('sun_gray.bmp')
	print("Image has been Taken")
	return(img) 

def serialConnectionCheck():            
	### Turn the Serial Protocol ON
	port = '/dev/ttyACM0'
	baud = 115200
	ser = serial.Serial(port, baud, timeout = 6)
	print("Serial Connection Setup")
	return ser
def wifiConnectionCheck():
	### Test wifi connection
	loop_value = 1
	while loop_value == 1:
		try:
			urllib.request.urlopen("http://google.com")
			loop_value=0
		except urllib.error.URLError as e:
			print(e.reason)
			f.write( "Network currently down." )
		import time
		time.sleep(5)
	else:
		print( "Wifi Connection is Up and Running." )
def ProtectionUnitCover(ser):
	### Get Weather codes
	topWeatherCodes=getWeatherForTop();
	WeatherStatus= topWeatherCodes['badWeatherNow']
	CoverStatus= topWeatherCodes['topCurrentStatus']
	print("Weather Status:")
	print(WeatherStatus)
	print("Cover Staus:")
	if CoverStatus == 1:
		print("Cover is Open")
	else:
		print("Cover is Closed")
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
def HourlySunPosition(ser):
	[motor_azimuth,motor_zenith]=hourly_position()
	val_vertical=str(motor_zenith[0])	
	val_horizontal=str(motor_azimuth[0])
	
	### Move Tracker	
	[old_i, old_j]= MotorMovementTracker(ser,val_vertical,val_horizontal)
	
	return(old_i, old_j)
def MotorMovementTracker( ser,val_vertical,val_horizontal):
	### Move Tracker
	import time
	print("Vertical Movement of Motor 1:")
	print(val_vertical)
	print("Horizontal Movemrnt of Motor 2:")
	print(val_horizontal)
	motor_ver='v'
	motor_hor='h'
	
	ser.write(motor_ver.encode('utf-8'))
	time.sleep(2)
	ser.write(val_vertical.encode('utf-8'))
	time.sleep(2)
	ver_pos=ser.read(10)
	time.sleep(2)
	ser.write(motor_hor.encode('utf-8'))
	time.sleep(2)
	ser.write(val_horizontal.encode('utf-8'))
	time.sleep(2)
	hor_pos=ser.read(10)
	time.sleep(2)
	
	#feedback into string
	ver_pos=str(ver_pos)
	hor_pos=str(hor_pos)
	# split string to get position
	old_i=ver_pos.split('\\r\\n')
	old_j=hor_pos.split('\\r\\n')
	
	#old_i=int(old_i[1])
	#old_j=int(old_j[1])

	return (int(val_vertical),int(val_horizontal))

def CheckSunCentered(ser,old_i, old_j):
	### Get image from camera
	img=cameraConnetion()
	
	### Find center of sun in image using image processing
	rp = region_properties()
	[xC, yC, height, width]=rp.GetCenter(img);
	print("Image is being processed:")
	#xC=234
	#yC=560
	#height=960
	#width=1200
	
	### Check if sun is in scope
	print("Checking to see if sun is centered in image:")
	[rightPixel, leftPixel, downPixel, upPixel]=pixel_distance(height/2, width/2, xC, yC)
	move=acceptedErrorCheck(rightPixel, leftPixel, downPixel, upPixel)
	if move ==1:
		print("Image is centered")
	else :
		print("Image is not centered. Adjust motors.")
		### Call function to see if image is centered
		AdjustTracker(old_i,old_j,move,img,height, width, rightPixel, leftPixel, downPixel, upPixel,ser)

#---- Adjusts Tracker until sun is centered in image----
def AdjustTracker(old_i,old_j,move,img,height, width, rightPixel, leftPixel, downPixel, upPixel, ser):
	#while (move == 1):
		### Get position of servos on mirror
		[iChange, jChange]=SunCenteredCheck(height, width, rightPixel, leftPixel, downPixel, upPixel)
		
		### Get old angle from servo motor
		
		### Calculate how far to move
		[motor_i, motor_j]=sendPosition(move, iChange, jChange,old_i, old_j)	
		print("New Vertical Movement of Motor 1:")
		print(motor_i)
		print("New Horizontal Movement of Motor 2:")
		print(motor_j)
		### Send move to Uno
		import time
		motor_ver='v';
		motor_hor='h';
		val_vertical=str(motor_i)
		val_horizontal=str(motor_j)
		ser.write(motor_ver.encode('utf-8'))
		time.sleep(2)
		ser.write(val_vertical.encode('utf-8'))
		time.sleep(2)
		ver_pos=ser.read(10)
		time.sleep(2)
		ser.write(motor_hor.encode('utf-8'))
		time.sleep(2)
		ser.write(val_horizontal.encode('utf-8'))
		time.sleep(2)
		hor_pos=ser.read(10)
		time.sleep(2)
		
		ver_pos=str(ver_pos)
		hor_pos=str(hor_pos)
		# split string to get position
		#old_i=ver_pos.split('\\r\\n')
		#print(old_i)
		#old_j=hor_pos.split('\\r\\n')
		
		#old_i=int(old_i[1])
		#old_j=int(old_j[1])
		
		### Get image from camera
		#img=cameraConnetion();
		
		### Find center of sun in image using image processing 
		#[xC, yC, height, width]=GetCenter(img);
		#xC=234
		#yC=560
		#height=960
		#width=1200
		
		### Check if sun is in scope
		#[rightPixel, leftPixel, downPixel, upPixel]=pixel_distance(height/2, width/2, xC, yC);
		#move=acceptedErrorCheck(rightPixel, leftPixel, downPixel, upPixel);
				
	### Save good image on computer
	#img.save(img)
ser=serialConnectionCheck() 
wifiConnectionCheck()
print("Checking Weather");
#CoverStatus=ProtectionUnitCover(ser)
#if CoverStatus == 1:
flag=0;
while(flag !=10):
	[old_i,old_j]=HourlySunPosition(ser);
	time.sleep(3)
	old_i=old_i+30;
	old_j=old_j-30;
	CheckSunCentered(ser,old_i, old_j);
	flag=flag+1;
	time.sleep(60)





