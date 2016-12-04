#!/usr/bin/python3

import os
import time
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from base import base

### Description: Using the apscheduler, the scheduler class manages the timing of the execution of functions
###				 
class scheduler(base):

	### Description: Initialize the scheduling object itself within this class
	### 			 cron like scheduling is used
	### 			 
	### What each option means:
	###		day='1-7' -- Schedule the function to be run every day, starting on Monday and ending on Sunday
	###		hour='8-17' -- Schedule the function to run from the hours 08:00 to 17:00 every hour
	###		hour='0-24/3' -- Schedule the function to run from the hours 00:00 to 24:00 every 3 hours
	### See: http://apscheduler.readthedocs.io/en/v3.3.0/modules/triggers/cron.html#module-apscheduler.triggers.cron
	def __init__(self):
		self.schedule = BlockingScheduler() # Initialize block type scheduler
		getTimeOfDay()
		self.schedule.add_job(CheckWeather, 'cron', day='1-7', hour='5-19/3')
		self.schedule.add_job(GetSunImage, 'cron', day='1-7', hour='8-17', minute='*/1')

	### Description: The scheduled function to check the weather
	### Flow: 	1) 
	### Input: 
	### Output: 
	### Example:
	### 	This function is not called from the class object, but called by the apscheduler object
	def CheckWeather(self):
		self.LogM(20, "Scheduled check for weather starting")
		# Do weather checking things
		# Add a debug statement with timestamp
		[CoverStatus]=ProtectionUnitCover();
		self.LogM(20, "Scheduled check for weather ending")
		return(CoverStatus)
		
	### Description: The scheduled function to capture sun images
	### Flow: 	1) 
	### Input: 
	### Output: 
	### Example:
	### 	This function is not called from the class object, but called by the apscheduler object
	def GetSunImage(self, CoverStatus):
		self.LogM(20, "Scheduled aquisition of the sun starting")
		# Do image getting things
		# Add a debug statement with timestamp
		if CoverStatus == 1:
			ser=serialConnectionCheck();
			[old_i, old_j]=HourlySunPosition(ser);
			CheckSunCentered(ser,old_i, old_j);
		self.LogM(20, "Scheduled aquisition of the sun ending")

	### Description: After adding all the jobs we want to the scheduler, we then start it
	def Start(self):
		self.LogM(20, "Starting the scheduler")
		self.schedule.start()

	### Description: To terminate the scheduler, we issue it the shutdown command
	###				 This will also terminate the program, so only use this if you want to end the program as a whole
	def End(self):
		self.LogM(20, "Ending the scheduler: shutting down")
		self.schedule.shutdown()
	
	### Description: Determines if it is currently daytime (8am - 5pm) or nighttime and stores it in instanced variables
	### 			 Taken from Tim's weather data parsing functionality. Including it here for a system wide function
	###				 Probably not needed, but including here for completeness
	### Flow: 	1) Get todays 8:10AM and 4:50PM time stamp
	###		2) Get timestamp for current time
	###		3) Determine whether day or night
	### Input: None
	### Output: None
	### Example:
	### 	
	def getTimeOfDay(self):
		### Get timestamp for current time
		self.timeString = datetime.datetime.now()									# Cali date and time datetime string
		self.timeFloat = datetime.datetime.timestamp(timeString)					# Convert to float time stamp
