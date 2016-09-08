#!/usr/bin/python3

import logging # We'll need this for all our logging purposes

# TODO: Test base class works properly, particularly the logging features
# TODO: Do multiple instances of logging interfere with each other when accessing the terminal?
# TODO: Once the above is complete, bless this or change as needed

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


    # When intializing the object, we will create handlers for the console and file output streams
    # 'Log_inst' is an instanced variable, only available to each instance of the object, not across the entire class inheritance
    # This will therefore keep each object's logging object separate from all the others.
    def __init__(self):
        self.Log_inst = logging.getLogger('__name__')
        log_filename = '__name__' + '.txt'
        self.Log_inst.basicConfig(datefmt=self.DATEFORMAT, format=self.FORMAT)
        # Set up two handlers, one to output at the DEBUG level to a file and other at the INFO level to the console
        self.Log_File = logging.FileHandler(log_filename)
        self.Log_File.setLevel(logging.DEBUG) # Set logging level to DEBUG
        self.Log_Console = logging.StreamHanler()
        self.Log_Console.setLevel(logging.INFO) # Set logging level to INFO
        # Add the handlers to Log_inst
        self.Log_inst.addHandler(self.Log_File)
        self.Log_inst.addHandler(self.Log_Console)

    ### Description: This is a wrapper function to make logging simpler than calling Log.debug or Log.info, etc
    ###
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
		self.Log_inst.log(level, message)