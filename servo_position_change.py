#!/usr/bin/python3

#Written By: Jacquelin Rodriguez
import os               																				
import datetime	
import time
import math
import cmath
import sched  

#----inputs for testing proposes-----
old_X= 100;
old_Y= 567;
imageCenter_x=640;
imageCenter_y=480;
sunCenter_x=696;
sunCenter_y=558;

#---Compute left, right, up, down pixel amounts from image center---
## left and right
if imageCenter_x > sunCenter_x:
	rightPixel= imageCenter_x-sunCenter_x;
else:
	rightPixel=0;
if imageCenter_x < sunCenter_x:
	leftPixel=	sunCenter_x-imageCenter_x;
else:
	leftPixel=0;

## up and down
if imageCenter_y > sunCenter_y:
	upPixel= imageCenter_y-sunCenter_y;
else:
	upPixel=0;
if imageCenter_y < sunCenter_y:
	downPixel=	sunCenter_y-imageCenter_y;
else:
	downPixel=0;	
	
#----image size---
imageWidth=imageCenter_x *2;
imageHeight=imageCenter_y *2;

#----Servo Angle Movemnet----
servoX=47;
servoY=38;

#----pixel per degree----
horizontal=imageWidth/servoX;
vertical=imageWidth/servoY;

#******New Position Calculation******

##----Azimuth Angle Change----
if rightPixel != 0:
	xChange= rightPixel/horizontal;
if leftPixel != 0:
	xChange=-(leftPixel/horizontal);
		
##----Zenith Angle Change-----
if upPixel != 0:
	yChange= -(upPixel/vertical);	
if downPixel != 0:
	yChange=downPixel/vertical;


##------normalize angles and truncate to 4 decimal places-----
x_angle = 0.3125*round(xChange/0.3125)
y_angle = 0.3125*round(yChange/0.3125)

def truncate (f, n):
 	s = '%.12f' % f
 	i, p, d = s.partition('.')
 	return ('.'.join([i, (d+'0'*n)[:n]]));
	
x_angle=truncate(x_angle, 4)
y_angle=truncate(y_angle, 4)

##-----New position angle-----
old_X=old_X*0.3125;
old_Y=old_Y*0.3125;

new_X= old_X+float(x_angle);
new_Y= old_Y+float(y_angle);

##---- motor command-------
motor_X=int(new_X/0.3125);
motor_Y=int(new_Y/0.3125);

