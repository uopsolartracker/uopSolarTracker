#!/usr/bin/python3

#Written By: Jacquelin Rodriguez
import os               																				
import datetime	
import time
import math
import cmath
import sched  

#---Compute left, right, up, down pixel amounts from image center---
def pixel_distance(imageCenter_i, imageCenter_j, sunCenter_i, sunCenter_j):

	## left and right
	if imageCenter_j > sunCenter_j:
		rightPixel= imageCenter_j-sunCenter_j;
	else:
		rightPixel=0;
	if imageCenter_j < sunCenter_j:
		leftPixel=	sunCenter_j-imageCenter_j;
	else:
		leftPixel=0;

	## up and down
	if imageCenter_i > sunCenter_i:
		upPixel= imageCenter_i-sunCenter_i;
	else:
		upPixel=0;
	if imageCenter_i < sunCenter_i:
		downPixel=	sunCenter_i-imageCenter_i;
	else:
		downPixel=0;
	return (rightPixel, leftPixel, downPixel, upPixel)		


def acceptedErrorCheck(rightPixel, leftPixel, downPixel, upPixel):
	flag1=0;
	flag2=0;
	### Checking to see if sun's center is within the range of acceptable error
	if (rightPixel > 100)  or (leftPixel > 100):
		flag1= 1;
	else:
		flag1=0;
	if (downPixel > 100 ) or (upPixel > 100):
		flag2=1;
	else: 
		flag2=0;
	### Checking to see if tracker has to be moved
	if (flag1== 1) or (flag2==1):
		move=1;
	elif (flag1== 1) and (flag2==1):
		move =1;
	else:
		move=0;
	return (move)	

def SunCenteredCheck(imageWidth, imageHeight, rightPixel, leftPixel, downPixel, upPixel):

	#----Servo Angle Movemnet----
	servo_j=47;
	servo_i=38;

	#----pixel per degree----
	horizontal=imageWidth/servo_j;
	vertical=imageHeight/servo_i;
	
	##----Azimuth Angle Change----
	if rightPixel != 0:
		jChange= rightPixel/horizontal;
	if leftPixel != 0:
		jChange=-(leftPixel/horizontal);
			
	##----Zenith Angle Change-----
	if upPixel != 0:
		iChange= -(upPixel/vertical);	
	if downPixel != 0:
		iChange=downPixel/vertical;	
			
	return(iChange, jChange)

def truncate (f, n):
	s = '%.12f' % f
	i, p, d = s.partition('.')
	return ('.'.join([i, (d+'0'*n)[:n]]));
			
def sendPosition(move,iChange, jChange, old_i, old_j):

	##------normalize angles and truncate to 4 decimal places-----
	j_angle = 0.325*round(jChange/0.325)
	i_angle = 0.325*round(iChange/0.325)
		
	j_angle=truncate(j_angle, 4)
	i_angle=truncate(i_angle, 4)

	j_angle=float(j_angle)
	i_angle=float(i_angle)

	##---- motor command-------
	motor_j=old_j+int(j_angle/0.325);
	motor_i=old_i+int(i_angle/0.325);
	
	return( motor_i, motor_j)


#[rightPixel, leftPixel, downPixel, upPixel]=pixel_distance(imageCenter_i, imageCenter_j, sunCenter_i, sunCenter_j)	
#[flag1, flag2]=acceptedErrorCheck(rightPixel, leftPixel, downPixel, upPixel)
#[move, iChange, jChange]=SunCenteredCheck(flag1, flag2)
#sendPosition(move, iChange, jChange)	
	
