#!/usr/bin/python3

import logging

class Base:
    FORMAT = '%(asctime)s -- %(module)s:%(funcName)s -- %(message)s'
    DATEFORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, log_filename):
        self.Log = logging.getLogger('__name__')
        self.Log.basicConfig(filename=self.log_filename, level=logging.DEBUG, datefmt=self.DATEFORMAT, format=self.FORMAT)

	# Level		Numeric value
	# CRITICAL		50
	# ERROR			40
	# WARNING		30
	# INFO			20
	# DEBUG			10
	# NOTSET		0
	def LogM(self, message, level):
		self.Log.log(level, message)
