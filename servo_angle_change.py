#!/usr/bin/python3

#Written By: Jacquelin Rodriguez
import math
import cmath

#----inputs for testing proposes-----
imageCenter_x=640
imageCenter_y=480
sunCenter_x=696
sunCenter_y=558

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
imageHeight=imageCenter_y*2;

#----Servo Angle Movemnet----
servoX=300;
servoY=300;

#----pixel per degree----
horizontal=imageWidth/servoX
vertical=imageWidth/servoY

#----Define variables---
xChange=0;
yChange=0;

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
	
##-----save new Position Angles to excel-----
print(xChange,yChange)
