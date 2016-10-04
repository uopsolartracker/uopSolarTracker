#!/usr/bin/python3

# Testing to communicate Arduino and Raspberry Pi 3

import serial
import time

d = '1'

port = '/dev/ttyACM0'
baud = 9600

ser = serial.Serial(port, baud, timeout = 3)

while True:

	if d == '150':
		print("Reached 150 max in pi")
		d = 1

	ser.write(d.encode('utf-8'))
	print('write\n')
	
	bytestoread = ser.inWaiting()
	d = ser.readline()[:-2].decode()
	print('Read = ', d) # truncate the \n\r

