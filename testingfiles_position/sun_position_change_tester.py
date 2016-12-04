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

from region_properties import region_properties
from servo_position_change import *

def cameraConnetion():
	img = cv2.imread('sun_gray.bmp')
	return(img) 

def serialConnectionCheck():            
	### Turn the Serial Protocol ON
	port = '/dev/ttyACM0'
	baud = 115200
	ser = serial.Serial(port, baud, timeout = 6)
	return ser
def CheckSunCentered(ser,old_i, old_j):
	### Get image from camera
	img=cameraConnetion()
	
	### Find center of sun in image using image processing
	rp = region_properties()
	[xC, yC, height, width]=rp.GetCenter(img);
	#xC=234
	#yC=560
	#height=960
	#width=1200
	
	### Check if sun is in scope
	[rightPixel, leftPixel, downPixel, upPixel]=pixel_distance(height/2, width/2, xC, yC)
	move=acceptedErrorCheck(rightPixel, leftPixel, downPixel, upPixel)
	
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
		old_i=ver_pos.split('\\r\\n')
		old_j=hor_pos.split('\\r\\n')
		print(old_i)
		old_i=int(old_i[1])
		old_j=int(old_j[1])
		
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
old_i=700
old_j=700
CheckSunCentered(ser,old_i, old_j)
