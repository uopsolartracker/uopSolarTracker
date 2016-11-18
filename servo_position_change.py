#!/usr/bin/python3

#Written By: Jacquelin Rodriguez
import os               																				
import datetime	
import time
import math
import cmath
import sched  

#----inputs for testing proposes-----
old_j= 100;
old_i= 567;

#----image size---
imageWidth=imageCenter_i *2;
imageHeight=imageCenter_j *2;

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
	if (rightPixel > 100)  or (leftPixel > 100):
		flag1= 1;
	else:
		flag1=0;
	if (downPixel > 100 ) or (upPixel > 100):
		flag2=1;
	else: 
		flag2=0;
	return (flag1, flag2)	

def SunCenteredCheck(flag1, flag2):
	iChange=0;
	jChange=0;
	if (flag1 == 1 or flag2 ==1):
		move=1;
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
	else:
		move=0;	
	return(move, iChange, jChange)

def truncate (f, n):
	s = '%.12f' % f
	i, p, d = s.partition('.')
	return ('.'.join([i, (d+'0'*n)[:n]]));
			
def sendPosition(move, iChange, jChange):
	motor_i=0;
	motor_j=0;
	if move == 1:
		##------normalize angles and truncate to 4 decimal places-----
		j_angle = 0.3125*round(jChange/0.3125)
		i_angle = 0.3125*round(iChange/0.3125)
			
		j_angle=truncate(j_angle, 4)
		i_angle=truncate(i_angle, 4)

		##-----New position angle-----
		old_j=old_j*0.3125;
		old_i=old_i*0.3125;

		new_j= old_j+float(j_angle);
		new_i= old_i+float(i_angle);

		##---- motor command-------
		motor_j=int(new_j/0.3125);
		motor_i=int(new_i/0.3125);
	else:
		move=0	
	return(move, motor_i, motor_j)


[rightPixel, leftPixel, downPixel, upPixel]=pixel_distance(imageCenter_i, imageCenter_j, sunCenter_i, sunCenter_j)	
[flag1, flag2]=acceptedErrorCheck(rightPixel, leftPixel, downPixel, upPixel)
[move, iChange, jChange]=SunCenteredCheck(flag1, flag2)
sendPosition(move, iChange, jChange)	
	
