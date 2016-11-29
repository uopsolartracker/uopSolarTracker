#!/usr/bin/python3

# Testing to communicate Arduino and Raspberry Pi 3

import serial
import time
import random

d = '1'

port = '/dev/ttyACM0'
baud = 115200

ser = serial.Serial(port, baud, timeout = 6)

def truncate (f, n):
	'''Truncate a float f to n decimal places without rounding'''
	s = '%.12f' % f
	i, p, d = s.partition('.')
	return ('.'.join([i, (d+'0'*n)[:n]]));



while True:

	#if d == '150':
	#	print("Reached 150 max in pi")
	#	d = 1
	
	val = input("Angle between -150 - 150: ")
	#val = 500

	if val == "r":	
		ser.write(val.encode('utf-8'))
	elif val == "stat":
		ser.write(val.encode('utf-8'))
	elif val == "v":
		ser.write(val.encode('utf-8'))
	elif val == "h":
		ser.write(val.encode('utf-8'))
	else:
		#val = int(val)
		#val = char(val)
		#val = random.uniform(-150,150)	# Generate random numbers between -150, 150 for simulated data
		#val = .325*round(val/.325)	# Normalize all values to be divisible by .325 (precision of motor)
		###val = truncate(val, 3)		# Truncate vals to 3 decimal points and convert to string to send over serial
		print(val)
		ser.write(val.encode('utf-8'))
		
		###time.sleep(3)			# wait 5 second
		
	#print('write\n')
	
	#bytestoread = ser.inWaiting()
	#d = ser.readline()[:-2].decode()
	#print('Read = ', d) # truncate the \n\r

