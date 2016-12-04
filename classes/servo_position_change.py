#!/usr/bin/python3

#Written By: Jacquelin Rodriguez
import os               																				
import datetime	
import time
import math
import cmath
import sched
from base import base

class servo_positioning(base):

	#---Compute left, right, up, down pixel amounts from image center---
	def pixel_distance(self, imageCenter_i, imageCenter_j, sunCenter_i, sunCenter_j):
		self.LogM(10, "Finding the pixel distances between the sun's center and the center of the sun")
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

		self.LogM(10, "Found the distances as right={r}, left={l}, down={d}, and up={u}".format(r=rightPixel,l=leftPixel,d=downPixel,u=upPixel))
		return (rightPixel, leftPixel, downPixel, upPixel)


	def acceptedErrorCheck(self, rightPixel, leftPixel, downPixel, upPixel):
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
			self.LogM(10, "The mirror needs to be moved")
		elif (flag1== 1) and (flag2==1):
			move =1;
			self.LogM(10, "The mirror needs to be moved")
		else:
			move=0;
			self.LogM(10, "The mirror does not need to be moved")
		return (move)	

	def SunCenteredCheck(self, imageWidth, imageHeight, rightPixel, leftPixel, downPixel, upPixel):

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

	def truncate (self, f, n):
		s = '%.12f' % f
		i, p, d = s.partition('.')
		return ('.'.join([i, (d+'0'*n)[:n]]));
				
	def sendPosition(self, move,iChange, jChange, old_i, old_j):

		##------normalize angles and truncate to 4 decimal places-----
		j_angle = 0.3125*round(jChange/0.3125)
		i_angle = 0.3125*round(iChange/0.3125)
			
		j_angle=truncate(j_angle, 4)
		i_angle=truncate(i_angle, 4)

		j_angle=float(j_angle)
		i_angle=float(i_angle)

		##---- motor command-------
		motor_j=old_j+int(j_angle/0.325);
		motor_i=old_i+int(i_angle/0.325);
		
		self.LogM(10, "Sending new coordinates to the motors: ({i}, {j})".format(i=motor_i,j=motor_j))
		return( motor_i, motor_j)


	#[rightPixel, leftPixel, downPixel, upPixel]=pixel_distance(imageCenter_i, imageCenter_j, sunCenter_i, sunCenter_j)	
	#[flag1, flag2]=acceptedErrorCheck(rightPixel, leftPixel, downPixel, upPixel)
	#[move, iChange, jChange]=SunCenteredCheck(flag1, flag2)
	#sendPosition(move, iChange, jChange)	
		
