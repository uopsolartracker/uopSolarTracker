#!/usr/bin/python3

#Written By: Jacquelin Rodriguez
import os               																				
import datetime	
import time
import math
import cmath
import sched  
import xlsxwriter 
from xlrd import open_workbook

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
imageHeight=imageCenter_y *2;

#----Servo Angle Movemnet----
servoX=47;
servoY=38;

#----pixel per degree----
horizontal=imageWidth/servoX
vertical=imageWidth/servoY
print(horizontal,vertical)
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

## ---getting servo position at this moment---
timeStamp= time.time();

# convert timestamp to humanreadable form
humanReadable_TS= datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d-%H-%M-%S');

# parse human readable to create variables for year, month, day, etc.
h = humanReadable_TS.split("-");

Hour_Lisit=[];
List =[];

Year = float (h[0]); # from humanreadable Year
Month = float(h[1]); # from humanreadable Month
Day = float(h[2]); # from humanreadable Day
hour= float(h[3]);
Minutes = float(30); # minutes set to 30
string_find= str(int(hour))+ ":" +str(int(Minutes))

book = open_workbook('sun_postion_data'+'_'+str(int(Month))+'_'+str(int(Day))+'_'+str(int(Year))+ '.xlsx')
for sheet in book.sheets():
    for rowidx in range(sheet.nrows):
        row = sheet.row(rowidx)
        for colidx, cell in enumerate(row):
            if cell.value == string_find :
                print (colidx)
                print (rowidx)


	
##------normalize angles and truncate to 3 decimal places-----
x_angle = 0.325*round(xChange/0.325)
y_angle = 0.325*round(yChange/0.325)

def truncate (f, n):
 	#Truncate a float f to n decimal places without rounding'''
 	s = '%.12f' % f
 	i, p, d = s.partition('.')
 	return ('.'.join([i, (d+'0'*n)[:n]]));
	
x_angle=truncate(x_angle, 3)
y_angle=truncate(y_angle, 3)

##-----save new Position Angles to excel-----
print(x_angle,y_angle)
	
	
