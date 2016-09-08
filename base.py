#!/usr/bin/python3

import logging # We'll need this for all our logging purposes

### Description: A "base" class from which all other objects will inherit. This will keep the logging centralized
### Flow: --> None
### Input: log_filename
### Output: None
### Example: class MyModule(base)
class base:
	# Formatting the output to be "2016:09:01 18:42:10 -- module_name:func_name -- the message"
    FORMAT = '%(asctime)s -- %(module)s:%(funcName)s -- %(message)s'
    # This actually formats the time stamp, otherwise we would have milliseconds included by default
    DATEFORMAT = '%Y-%m-%d %H:%M:%S'

    # When intializing the object, we will pass it the file name we want it to output to
    # Everything else will be handled without needing any input
    # 'Log' is an instanced variable, only available to each instance of the object, not across the entire class inheritance
    def __init__(self, log_filename):
        self.Log = logging.getLogger('__name__')
        self.Log.basicConfig(filename=self.log_filename, level=logging.DEBUG, datefmt=self.DATEFORMAT, format=self.FORMAT)

    ### Description: This is a wrapper function to make logging simpler than calling Log.debug or Log.info, etc
	### Flow: --> Take in numeric value corresponding to the logging level, and the message
	###		--> Call the logging object in the class to log the message at the right level
	### Input: level, message
	### Output: None
	### Example: MyModule.Log(10, "This function is working")
	#
	# Below are the logging levels and their corresponding numeric values.
	# It is also possible to create our own logging levels; probably not necessary
	#
	# Level		Numeric value
	# CRITICAL		50
	# ERROR			40
	# WARNING		30
	# INFO			20
	# DEBUG			10
	# NOTSET		0
	def LogM(self, level, message):
		self.Log.log(level, message)
