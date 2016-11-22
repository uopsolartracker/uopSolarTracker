#!/usr/bin/python3

import sched
import time
import datetime

### Description: 
class scheduler(object):
	# Used for checking against when we last checked in
	last_check = 0
	# The psuedo-constants we will need
	TENMINUTES = 600
	THREEHOURS = 10800

	# Initialize the scheduling object itself within this class
	def __init__(self):
		self.schedule = sched(time.time, time.sleep)

	def periodic(self, interval, action, actionargs=()):
		self.scheduler.enter(interval, 1, periodic, (scheduler, interval, action, actionargs))
		action(*actionargs)

	def StartDay():

	def EndDay():

	def CheckWeather():

	def GetSunImage():
	
	### Description: Determines if it is currently daytime (8am - 5pm) or nighttime.
	### 			 Taken from Tim's weather data parsing functionality. Including it here for a system wide function
	### Flow: 	1) Get todays 8:10AM and 4:50PM time stamp
	###		2) Get timestamp for current time
	### Input: 
	### Output: 
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

		### 3) Set index if during day
		if self.timeFloat >= self.eightTenAM and self.timeFloat <= self.fourFiftyPM:
			#print("DAY = ", topCoverCodes['dayTime'])
			return
		
		return

