#!/usr/bin/python3

import os
import time
import datetime
from apscheduler.schedulers import BlockingScheduler

### Description: 
class scheduler(object):
	# Used for checking against when we last checked in
	last_check = 0
	# The psuedo-constants we will need
	TENMINUTES = 600
	THREEHOURS = 10800

	# Initialize the scheduling object itself within this class
	def __init__(self):
		self.schedule = BlockingScheduler()
		getTimeOfDay()
		self.schedule.add_job(CheckWeather, 'interval', hours=3)

	def CheckWeather(self):

	def GetSunImage(self):

	def StartDay(self):
		self.schedule.start()

	def EndDay(self):
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
		### 1) Get todays 8:10AM and 4:50PM timestamp
		self.eightTenAMString = str(datetime.date.today()) + ' 08:10:0'
		self.eightTenAM = datetime.datetime.strptime(eightTenAMString, "%Y-%m-%d %H:%M:%S").timestamp()	# float type
		self.fourFiftyPMString = str(datetime.date.today()) + ' 16:50:0'
		self.fourFiftyPM = datetime.datetime.strptime(fourFiftyPMString, "%Y-%m-%d %H:%M:%S").timestamp()	# float type

		### 2) Get timestamp for current time
		self.timeString = datetime.datetime.now()									# Cali date and time datetime string
		self.timeFloat = datetime.datetime.timestamp(timeString)					# Convert to float time stamp

		### 3) Set if during day
		self.isday = 0
		if self.timeFloat >= self.eightTenAM and self.timeFloat <= self.fourFiftyPM:
			self.isday = 1