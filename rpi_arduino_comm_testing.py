#!/usr/bin/python3

# Testing to communicate Arduino and Raspberry Pi 3

import serial

port = '/dev/ttyACM0'
baud = 9600

ser = serial.Serial(port, baud, timeout = 1)

while True:
	ser.write('87\n'.encode('utf-8'))
	print('write\n')
	print('Read = ', ser.readline()[:-2].decode());	# truncate the \n\r

