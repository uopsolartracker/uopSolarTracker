#!/usr/bin/python3

import os               																				
import math
import cmath
import sched  
import serial
import urllib
import time
import datetime


from region_properties import*
from servo_position_change import *

def cameraConnetion():

	return(img) 

def CheckSunCentered(ser,old_i, old_j):
	### Get image from camera
	[img]=cameraConnetion()
	
	### Find center of sun in image using image processing 
	[xC, yC, height, width]=GetCenter(img);
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