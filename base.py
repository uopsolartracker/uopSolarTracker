#!/usr/bin/python3

import logging # We'll need this for all our logging purposes
from time import strftime, localtime

# TODO: Find a way to name the classes which inherit from base, without feeding in names for the logging handlers and files
# TODO: Once the above is complete, bless this or change as needed

### Description: A "base" class from which all other objects will inherit. This will keep the logging centralized
### Flow: --> None
### Input: log_filename
### Output: None
### Example: class MyModule(base)
class base:
    # Formatting the output to be "2016:09:01 18:42:10 -- module_name:func_name -- the message"
    FORMAT = '%(asctime)s -- %(module)s:%(funcName)s:%(levelname)s -- %(message)s'
    # This actually formats the time stamp, otherwise we would have milliseconds included by default
    DATEFORMAT = '%Y-%m-%d %H:%M:%S'


    # When intializing the object, we will create handlers for the console and file output streams
    # 'Log_inst' is an instanced variable, only available to each instance of the object, not across the entire class inheritance
    # This will therefore keep each object's logging object separate from all the others.
    #
    # The best part of this is we do not need to specify whether to output to the console, file, or both, 
    # since the handlers will automatically filter the logging statements based on level
    def __init__(self):
        self.Log_inst = logging.getLogger(strftime("%a, %d %b %Y %H:%M:%S", localtime()))
        log_filename = strftime("%Y %d %b %H-%M-%S", localtime()) + '.txt'
        logging.basicConfig(level='DEBUG',format=self.FORMAT, datefmt=self.DATEFORMAT,filename=log_filename)

        # Set a handler, at the INFO level to output to the console
        self.Log_Console = logging.StreamHandler() # Output will go to the console
        self.Log_Console.setLevel('INFO') # Set logging level to INFO
        self.Log_Console.setFormatter(logging.Formatter(self.FORMAT,self.DATEFORMAT))

        # Add the handler to Log_inst
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
    # It is also possible to create our own logging levels; not necessary
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