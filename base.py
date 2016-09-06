#!/usr/bin/python3

import logging

class base:
	LOG_FILENAME = 'Log_File.txt'
	FORMAT = '%(asctime)s -- %(module)s:%(funcName)s -- %(message)s'
	DATEFORMAT = '%Y-%m-%d %H:%M:%S'

	def __init__(self):
		self.Log = logging.getLogger('__name__')
		Log.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,datefmt=DATEFORMAT,format=FORMAT)

# Level		Numeric value
# CRITICAL		50
# ERROR			40
# WARNING		30
# INFO			20
# DEBUG			10
# NOTSET		0
	def LogM(self,message,level):
		Log.log(level, message)