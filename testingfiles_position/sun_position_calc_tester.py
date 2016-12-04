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
#import sun_position_calc
def serialConnectionCheck():            
	### Turn the Serial Protocol ON
	port = '/dev/ttyACM0'
	baud = 115200
	ser = serial.Serial(port, baud, timeout = 6)
	return ser
	
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
	old_i=int(old_i[1])
	old_j=int(old_j[1])
	return (old_i,old_j)


ser =serialConnectionCheck()
HourlySunPosition(ser)
