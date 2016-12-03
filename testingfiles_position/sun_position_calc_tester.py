#!/usr/bin/python3
import os               																				
import math
import cmath
import sched  
import serial
import urllib
import time
import datetime


from sun_position_calc import *

def serialConnectionCheck():            
	### Turn the Serial Protocol ON
	port = '/dev/ttyACM0'
	baud = 9600
	ser = serial.Serial(port, baud, timeout = 6)
	return ser
	
def HourlySunPosition(ser):
	[motor_azimuth,motor_zenith]=_hourly_position_();
	val_vertical=str(y_zenith[0]);	
	val_horizontal=str(x_azimuth[0]);
	
	### Move Tracker	
	[old_i, old_j]= MotorMovementTracker(ser,val_vertical,val_horizontal);
	
	return(old_i, old_j)
def MotorMovementTracker( ser,val_vertical,val_horizontal):
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
