#!/usr/bin/python3

import os               											# Allow interaction with operating system modules
import urllib.request											# urllib for python3, need to get url of OpenWeatherMap
															# https://docs.python.org/3/library/urllib.request.html#urllib.request.Request
import json													# Default data from API is in JSON format so need this module to parse it
															# https://docs.python.org/3/library/json.html?highlight=json#module-json
import datetime												# Used to get a human-readable timestamp
															# https://docs.python.org/3/library/datetime.html#module-datetime
from collections import OrderedDict								# Used to order the JSON data from the API in the same order it is imported as. Otherwise, output is unordered

#TODO: add exception handling
#TODO: save top closing data to file/webpage, when and why it closed
#TODO: Make input files to test all weather possibilities to see if desired result is achived

# Time Defines (seconds)
TENMINUTES = 600.0
THREEHOURS = 10800

topCoverCodes = {
			"topCurrentStatus": 0,		# Status of top cover: 	0 = closed, 1 = open
			"dayTime": 0,			# Status of daylight: 	0 = night, 1 = day
			"badWeatherNow": 0,		# Status of current weather:	0 = good weather, 1 = bad weather
			"nextAPIPoint": 0,		# Status of closest API given forecast time: 	0 = good weather, 1 = bad weather
			"weatherEightAM": 0,		# Status of weather at 8am:	0 = good weather, 1 = bad weather
			"weatherElevenAM": 0,		# Status of weather at 11am:	0 = good weather, 1 = bad weather
			"weatherTwoPM": 0,		# Status of weather at 2pm:	0 = good weather, 1 = bad weather
			"weatherFivePM": 0,		# Status of weather at 5pm:	0 = good weather, 1 = bad weather
			"currentWeatherTime": 0.0,	# Timestamp of when weather last checked. Used to check when 10min elapsed since last check
			"eightAMTimestamp": 0.0,	# Timestamp of date + 8am. Used to find time-gap to open top
			"elevenAMTimestamp": 0.0,	# Timestamp of date + 11am. Used to find time-gap to open top
			"twoPMTimestamp": 0.0,		# Timestamp of date + 2pm. Used to find time-gap to open top
			"fivePMTimestamp": 0.0,		# Timestamp of date + 5pm. Used to find time-gap to open top
			"gapStart": 0.0,		# Timestamp of when to allow top to open
			"gapEnd": 0.0			# Timestamp of when to allow top to close
			}

### Prepare request for weather data (comes in JSON format) from OpenWeatherMap.com
zipCode = "95211"															# University of the Pacific zipcode = 95211
APIKey = "849eb6e48e5b5e037e1cb47efea60d62"

urlForecastBase = "http://api.openweathermap.org/data/2.5/forecast?q="
forecastURL = urlForecastBase + zipCode + ",us&APPID=" + APIKey					# Forecast URL of OpenWeatherMap API

urlWeatherBase = "http://api.openweathermap.org/data/2.5/weather?q="
weatherURL = urlWeatherBase + zipCode + ",us&APPID=" + APIKey					# Current weather URL of OpenWeatherMap API

### Read in text file of weather codes into a python dictionary
idCodeDictionary = {}
descriptionCodeDictionary = {}
with open('weatherCodes.txt', 'r') as weatherCodes:
	skipFirstLine = next(weatherCodes)											# Skip first line of text file
	for line in weatherCodes:
		splitLine = line.split()
		descriptionCodeDictionary[int(splitLine[0])] = ", ".join(splitLine[1:])			# Capture description
		idCodeDictionary[int(splitLine[0])] = ", ".join(splitLine[1])					# Do not capture description

print("Init topCoverCodes = ", json.dumps(topCoverCodes, sort_keys=True, indent=4))

#example http://api.openweathermap.org/data/2.5/weather?q=65065us&APPID=849eb6e48e5b5e037e1cb47efea60d62

### Description: Gets current weather and sets badWeatherNow attribute. Is to be called from main.
### Flow: 	--> Get time of day
###		--> Call forecast API 
###		--> Parse incoming JSON 
###		--> Convert times to local time
###		--> Check API weather code against code in idCodeDictionary to see if bad weather
###		--> Set bad weather indicator by setting topCoverCodes['badWeatherNow'] = 1 and saves time
### Input: topCoverCodes
### Output: topCoverCodes
### Example:
### 	Call getWeatherForTop() from main --> sets topCoverCodes.topCurrentStatus = 0 (good weather) or 1 (bad weather)
def getWeatherForTop():
	""" Sets current weather ID and time """

	print("Inside getWEATHERfortop......................")		

	# Get time of day
	getTimeOfDay()

	# Get the API response of the current weather data
	url = weatherURL
	jsonStringWeather = requestAPI(url)

	# Parse the current weather data
	weatherID = jsonStringWeather['weather'][0]['id']
	weatherLocalTimeString = datetime.datetime.fromtimestamp(jsonStringWeather['dt'])	# Local time datetime.datetime type string
	weatherLocalTimestamp = datetime.datetime.strptime(str(weatherLocalTimeString), "%Y-%m-%d %H:%M:%S").timestamp()	# float type
	print("Current ID: ", weatherID, "	Time: ", weatherLocalTimeString, "	Stamp: ", weatherLocalTimestamp)
	
	# Check ID against ID code file to see if bad weather, x = bad weather in text file
	if idCodeDictionary[weatherID] == 'x':
		topCoverCodes['badWeatherNow'] = 1
	elif idCodeDictionary[weatherID] == '-':
		topCoverCodes['badWeatherNow'] = 0
	
	topCoverCodes['currentWeatherTime'] = weatherLocalTimestamp
			
	return topCoverCodes

### Description: Gets current forecast and sets time-gap to allow top to open. Is to be called from main.
### Flow: 	1) Call forecast API and save returned JSON string
###		2) Check if night or day
###			2.1) Night:
###				2.1.1) Find and set a time-gap to allow the top to open
###			2.2) Day:
###				2.2.1) Get current weather
###				2.2.2) Close now if bad weather, otherwise continue to next step
###				2.2.3) Find and set a time-gap to allow the top to open
### Input: topCoverCodes
### Output: topCoverCodes
### Example:
### 	Call getForecastForTop() from main --> check gap times to see when to open top, assumung there is a gap
def getForecastForTop():
	"""Returns a list of codes of weather to open the top cover of the protection unit or not"""
	
	print("Inside getForecastForTop...............")	
	
	### 1) Get the API response of the forecast data
	url = forecastURL
	jsonStringForecast = requestAPI(url)

	### Parse the forecast data into a lists TODO: PROB DONT NEED THIS SECTION
	forecastID = [ ]
	forecastTime = [ ]
	for i in range(jsonStringForecast['cnt']):									# 'cnt' is the count of lines returned by the API
		forecastID.append(jsonStringForecast['list'][i]['weather'][0]['id'])			# Create a list of forecasted weather ID's
		
		### Convert API time of forecast (UNIX) to local time and save in list
		# First convert to a string in local time
		forecastLocalTimeString = datetime.datetime.fromtimestamp(jsonStringForecast['list'][i]['dt'])
		# Next convert the local time string to a local time timstamp
		forecastLocalTimestamp = datetime.datetime.strptime(str(forecastLocalTimeString), "%Y-%m-%d %H:%M:%S").timestamp()
		# Create a list of forecast time timestamp data as a float
		forecastTime.append(forecastLocalTimestamp)

		print(i, ":	ID: ", forecastID[i], "	Time: ", forecastLocalTimeString, "	Stamp: ", forecastTime[i])

	### 2) Check if night or day ( day = anytime between 8:10am and 4:50pm), sets ['dayTime'] = 1/0
	getTimeOfDay()
	#print("getTimeOfDay in FORECAST = ", topCoverCodes)
	### 2.1) Night time
	if topCoverCodes['dayTime'] == 0:
		print("NIGHT")
		### 2.1.1) Find times to open the top cover
		findOpenTimes(jsonStringForecast)			
	### 2.2) Day time
	elif topCoverCodes['dayTime'] == 1:
		print("DAY")
		### 2.2.1) Check weather now
		getWeatherForTop(topCoverCodes)		
		if topCoverCodes['badWeatherNow'] == 1:
			### 2.2.2) # Close the top now if bad weather. TODO: Maybe hard code a 'close top' command to Arduino here or create an interrupt
			topCoverCodes['topCurrentStatus'] = 0
		### 2.2.3) Find times to open the top
		findOpenTimes(jsonStringForecast)		

	return topCoverCodes
	
	#outFile = open('Close_Top_Logs.txt', 'a')									# Open file to prepare for write

### Description: Gets JSON string dictionary response of weather/forecast data
### Flow: 	1) Open the URL
###		2) Save response to a string
### Input: url (url of weather or forecast)
### Output: jsonString (either weather or forecast data JSON string)
### Example:
### 	Call requestAPI() from getWeatherForTop or getForecastForTop to use the returned JSON data string
###	to find current weather or forecast weather at points in time.
def requestAPI(url):
	""" Request and read the API page """

	### 1) urlopen returns a bytes object so decode it so it can be read by the JSON module
	apiResponse = urllib.request.urlopen(url).read().decode('utf-8')
	#TODO: Close the URL with .close()
	### 2) Deserialize the JSON data to a string
	jsonString = json.loads(apiResponse, object_pairs_hook=OrderedDict)

	return jsonString

def getTopCoverStatus():
	""" Sets open/close index based on other closeTopCoverCodes indicies and returns closeTopCoverCodes to the main function """

### Description: Finds all good weather time-gaps and sets a time to allow top to open based on when
###		 the good weather gaps are in time.
### Flow: 	1) Loop over each iteration of jsonStringForecast until hit 8am then save those times and forecast until 5pm
###		2) Based on when there is good weather, set up a time-gap to allow the top to open by processing the data
### Input: topCoverCodes, jsonStringForecast
### Output: none
### Example:
### 	Call this function from getForecastForTop() to see when to open the top cover
def findOpenTimes(jsonStringForecast):
	""" Top Level to find times to allow th top cover to open """

	print("Inside findOPENtimes")

	### 1) Gather forecast for the day ahead starting at 8AM
	# Gather the forecast by iterating through the JSON string to find the time and weather ID of each 3-hour
	# forecast increment given by the API. Each iteration is 3 hours later and there is no forecast inbeween
	# each 3 hours timeframe.
	exitLoop = False
	# j is used as the iterator to iterate through the JSON string
	j = 0		
	# Loop until day time then fill truth table for open top times
	while exitLoop == False:
		# At each iteration, check if have reached an 8AM forecast then capture its weather and time.
		# If iteration started between 8AM-5PM, the data up to 5PM will be captured only.
		exitLoop = fillTable(jsonStringForecast, j)
		j = j + 1
	
	### 2) Set gaps of time when good weather
	processForecastConditions()	
	
	return

### Description: Determines if it is currently daytime (8am - 5pm) or nighttime.
### Flow: 	1) Get todays 8:10AM and 4:50PM time stamp
###		2) Get timestamp for current time
###		3) Set topCoverCodes index if during the day
### Input: topCoverCodes
### Output: topCoverCodes
### Example:
### 	Call this function from getForecastForTop() to set times when there is good weather during the daytime so top can open
def getTimeOfDay():
	""" Sets time index to 1 if currently between 8:10am and 4:50pm when there is light. This allows top to open if during the day. """
	
	### 1) Get todays 8:10AM and 4:50PM timestamp
	eightTenAMString = str(datetime.date.today()) + ' 08:10:0'
	eightTenAM = datetime.datetime.strptime(eightTenAMString, "%Y-%m-%d %H:%M:%S").timestamp()	# float type
	fourFiftyPMString = str(datetime.date.today()) + ' 16:50:0'
	fourFiftyPM = datetime.datetime.strptime(fourFiftyPMString, "%Y-%m-%d %H:%M:%S").timestamp()	# float type

	### 2) Get timestamp for current time
	timeString = datetime.datetime.now()											# Cali date and time datetime string
	timeFloat = datetime.datetime.timestamp(timeString)								# Convert to float time stamp

	### 3) Set index if during day
	if timeFloat >= eightTenAM and timeFloat <= fourFiftyPM:
		topCoverCodes['dayTime'] = 1
		#print("DAY = ", topCoverCodes['dayTime'])
		return
	topCoverCodes['dayTime'] = 0
	
	return

### Description: Sets weather status at 8am, 11am, 2pm, and/or 5pm by checking time at the current
###		 iteration of j from findOpenTimes function. j is iterated until 8am, 11am, 2pm, or 5pm
###		 has been encountered.
### Flow: 	1) Save time of j iteration that was passed in. It could be 8am, 11am, 2pm, or 5pm
###		2) Check the time to see if 8am, 11am, 2pm, or 5pm
###			2.1) Fill truth table inputs
###			2.2) Fill timestamps with real times then convert and save the times
### 			2.3) Set other values to 0 so that combination will get processed correctly in truth table
### Input: topCoverCodes, jsonStringForecast, j
### Output: true/false
### Example:
### 	Call this function from findOpenTimes() to set truth table to be processed to find then time-gaps are
def fillTable(jsonStringForecast, j):
	""" Saves time of day to open top and sets up truth table for when there is bad weather. """ 

	print("Inside FILLTABLE")

	###TODO: Maybe make a function for the code below.
	### 1) Save time of j iteration that was passed in. It could be 8am, 11am, 2pm, or 5pm
	forecastLocalTimeString = str(datetime.datetime.fromtimestamp(jsonStringForecast['list'][j]['dt']))		# gives in local time
	
	### 2) Check the time to see if 8am, 11am, 2pm, or 5pm
	if forecastLocalTimeString[11:] == "08:00:00":		
		### Get forecast between 8am - 5pm.
		# [j] = 8am, [j+1] = 11am, [j+2] = 2pm, [j+3] = 5pm
		# Fills truth table inputs, x = bad weather
		
		print("In fillTable 8AM")

		### 2.1) Fill truth table inputs
		if idCodeDictionary[jsonStringForecast['list'][j]['weather'][0]['id']] == 'x':
			topCoverCodes["weatherEightAM"] = 1

		if idCodeDictionary[jsonStringForecast['list'][j+1]['weather'][0]['id']] == 'x':
			topCoverCodes["weatherElevenAM"] = 1

		if idCodeDictionary[jsonStringForecast['list'][j+2]['weather'][0]['id']] == 'x':
			topCoverCodes["weatherTwoPM"] = 1	

		if idCodeDictionary[jsonStringForecast['list'][j+3]['weather'][0]['id']] == 'x':
			topCoverCodes["weatherFivePM"] = 1

		### 2.2) Fill 8-5 timestamps with real times. Convert and save the times
		# 8AM
		forecastLocalTimeString = datetime.datetime.fromtimestamp(jsonStringForecast['list'][j]['dt'])
		topCoverCodes["eightAMTimestamp"] = datetime.datetime.strptime(str(forecastLocalTimeString), "%Y-%m-%d %H:%M:%S").timestamp()	
		# 11AM
		forecastLocalTimeString = datetime.datetime.fromtimestamp(jsonStringForecast['list'][j+1]['dt'])
		topCoverCodes["elevenAMTimestamp"] = datetime.datetime.strptime(str(forecastLocalTimeString), "%Y-%m-%d %H:%M:%S").timestamp()
		# 2PM
		forecastLocalTimeString = datetime.datetime.fromtimestamp(jsonStringForecast['list'][j+2]['dt'])
		topCoverCodes["twoPMTimestamp"] = datetime.datetime.strptime(str(forecastLocalTimeString), "%Y-%m-%d %H:%M:%S").timestamp()	
		# 5PM				
		forecastLocalTimeString = datetime.datetime.fromtimestamp(jsonStringForecast['list'][j+3]['dt'])
		topCoverCodes["fivePMTimestamp"] = datetime.datetime.strptime(str(forecastLocalTimeString), "%Y-%m-%d %H:%M:%S").timestamp()

		print("TopCoverCodes = ",json.dumps(topCoverCodes, sort_keys=True, indent=4))
		print(" ")
	
		return True
	elif forecastLocalTimeString[11:] == "11:00:00":		
		### Get forecast between 11am - 5pm.
		# [j] = 11am, [j+1] = 2pm, [j+2] = 5pm
		# Fills truth table inputs

		print("In fillTable 11AM")
	
		if idCodeDictionary[jsonStringForecast['list'][j]['weather'][0]['id']] == 'x':
			topCoverCodes["weatherElevenAM"] = 1

		if idCodeDictionary[jsonStringForecast['list'][j+1]['weather'][0]['id']] == 'x':
			topCoverCodes["weatherTwoPM"] = 1	

		if idCodeDictionary[jsonStringForecast['list'][j+2]['weather'][0]['id']] == 'x':
			topCoverCodes["weatherFivePM"] = 1

		### Fill 11-5 timestamps with real times. Convert and save the times
		# 11AM
		forecastLocalTimeString = datetime.datetime.fromtimestamp(jsonStringForecast['list'][j]['dt'])
		topCoverCodes["elevenAMTimestamp"] = datetime.datetime.strptime(str(forecastLocalTimeString), "%Y-%m-%d %H:%M:%S").timestamp()
		# 2PM
		forecastLocalTimeString = datetime.datetime.fromtimestamp(jsonStringForecast['list'][j+1]['dt'])
		topCoverCodes["twoPMTimestamp"] = datetime.datetime.strptime(str(forecastLocalTimeString), "%Y-%m-%d %H:%M:%S").timestamp()	
		# 5PM				
		forecastLocalTimeString = datetime.datetime.fromtimestamp(jsonStringForecast['list'][j+2]['dt'])
		topCoverCodes["fivePMTimestamp"] = datetime.datetime.strptime(str(forecastLocalTimeString), "%Y-%m-%d %H:%M:%S").timestamp()
		
		print("TopCoverCodes = ", json.dumps(topCoverCodes, sort_keys=True, indent=4))
		print(" ")

		### 2.3) Set other values to 0 so that combination will get processed correctly
		resetCodesAndTimes(1)

		return True
	elif forecastLocalTimeString[11:] == "14:00:00":		
		### Get forecast between 2pm - 5pm.
		# [j] = 2pm, [j+1] = 5pm
		# Fills truth table inputs
	
		print("In fillTable 2PM")

		if idCodeDictionary[jsonStringForecast['list'][j]['weather'][0]['id']] == 'x':
			topCoverCodes["weatherTwoPM"] = 1	

		if idCodeDictionary[jsonStringForecast['list'][j+1]['weather'][0]['id']] == 'x':
			topCoverCodes["weatherFivePM"] = 1

		### Fill 2-5 timestamps with real times. Convert and save the times
		# 2PM
		forecastLocalTimeString = datetime.datetime.fromtimestamp(jsonStringForecast['list'][j]['dt'])
		topCoverCodes["twoPMTimestamp"] = datetime.datetime.strptime(str(forecastLocalTimeString), "%Y-%m-%d %H:%M:%S").timestamp()	
		# 5PM				
		forecastLocalTimeString = datetime.datetime.fromtimestamp(jsonStringForecast['list'][j+1]['dt'])
		topCoverCodes["fivePMTimestamp"] = datetime.datetime.strptime(str(forecastLocalTimeString), "%Y-%m-%d %H:%M:%S").timestamp()
		
		print("TopCoverCodes = ", json.dumps(topCoverCodes, sort_keys=True, indent=4))
		print(" ")

		### Set other values to 0 so that combination will get processed correctly
		resetCodesAndTimes(2)

		return True
	elif forecastLocalTimeString[11:] == "17:00:00":		
		### Get forecast at 5pm.
		# [j] = 5pm
		# Fills truth table inputs
	
		print("In fillTable 5PM")

		if idCodeDictionary[jsonStringForecast['list'][j]['weather'][0]['id']] == 'x':
			topCoverCodes["weatherFivePM"] = 1
		
		### Fill 5pm timestamp with real times. Convert and save the time
		# 5PM				
		forecastLocalTimeString = datetime.datetime.fromtimestamp(jsonStringForecast['list'][j+1]['dt'])
		topCoverCodes["fivePMTimestamp"] = datetime.datetime.strptime(str(forecastLocalTimeString), "%Y-%m-%d %H:%M:%S").timestamp()
		
		print("TopCoverCodes = ", json.dumps(topCoverCodes, sort_keys=True, indent=4))
		print(" ")

		### Set other values to 0 so that combination will get processed correctly
		resetCodesAndTimes(3)

		return True
	
	return False

### Description: Sets time-gaps of good weather based on saved times of forecast. Truth table will be filled by this point.
### Flow: 		1) Set any time-gap times reduced by 10min on each side
###			2) Clear all values for next time to be processed. Only need to preserve gap times.
### Input: topCoverCodes
### Output: topCoverCodes
### Example:
### 	Call this function from findOpenTimes() to get the time-gaps of when to open the top
def processForecastConditions():
	"""This function sets the time period to allow the top cover to open based on when there is good weather in the daytime."""

	print("Inside processFORECASTCONDITIONS")

		# bad weather == 1
		# Could have bad weather before a 1 or after so only okay to open if 2 consecutive 0's 
		# 8AM | 11AM | 2PM | 5PM || Allow Open for that Day
		# ------------------------------------------------------------------------
# 0		#    0    |     0     |    0    |    0    || 	8:10am - 4:50pm
# 1		#    0    |     0     |    0    |    1    || 	8:10am - 1:50pm
# 2		#    0    |     0     |    1    |    0    || 	8:10am - 10:50am
# 3		#    0    |     0     |    1    |    1    || 	8:10am - 10:50am
# 4		#    0    |     1     |    0    |    0    || 	2:10pm - 4:50pm
		#    0    |     1     |    0    |    1    ||  		     0
		#    0    |     1     |    1    |    0    ||  		     0
		#    0    |     1     |    1    |    1    ||  		     0
# 8		#    1    |     0     |    0    |    0    || 	11:10am - 4:50pm
		#    1    |     0     |    0    |    1    ||  		     0
		#    1    |     0     |    1    |    0    ||  		     0
		#    1    |     0     |    1    |    1    ||  		     0
#12 		#    1    |     1     |    0    |    0    || 	2:10pm - 4:50pm
		#    1    |     1     |    0    |    1    ||  		     0
		#    1    |     1     |    1    |    0    ||  		     0
		#    1    |     1     |    1    |    1    ||  		     0	
	
	### 1) Set any time-gap times reduced by 10min on each side
	# 0
	if topCoverCodes["weatherEightAM"] == 0 and topCoverCodes["weatherElevenAM"] == 0 and topCoverCodes["weatherTwoPM"] == 0 and topCoverCodes["weatherFivePM"] == 0:
		print("In process, #0")
		# If daytime, find when to start the gap time
		if topCoverCodes["dayTime"] == 1:
			gap_day_time(0)
		elif topCoverCodes["dayTime"] == 0:
			topCoverCodes["gapStart"] =  topCoverCodes["eightAMTimestamp"] + TENMINUTES
			topCoverCodes["gapEnd"] =  topCoverCodes["fivePMTimestamp"] - TENMINUTES

	# 1
	elif topCoverCodes["weatherEightAM"] == 0 and topCoverCodes["weatherElevenAM"] == 0 and topCoverCodes["weatherTwoPM"] == 0 and topCoverCodes["weatherFivePM"] == 1:
		print("In process, #1")
		if topCoverCodes["dayTime"] == 1:
			gap_day_time(1)
		elif topCoverCodes["dayTime"] == 0:		
			topCoverCodes["gapStart"] =  topCoverCodes["eightAMTimestamp"] + TENMINUTES
			topCoverCodes["gapEnd"] =  topCoverCodes["twoPMTimestamp"] - TENMINUTES
	
	# 2
	elif topCoverCodes["weatherEightAM"] == 0 and topCoverCodes["weatherElevenAM"] == 0 and topCoverCodes["weatherTwoPM"] == 1 and topCoverCodes["weatherFivePM"] == 0:
		print("In process, #2")
		if topCoverCodes["dayTime"] == 1:
			gap_day_time(2)
		elif topCoverCodes["dayTime"] == 0:
			topCoverCodes["gapStart"] =  topCoverCodes["eightAMTimestamp"] + TENMINUTES
			topCoverCodes["gapEnd"] =  topCoverCodes["elevenAMTimestamp"] - TENMINUTES

	# 3
	elif topCoverCodes["weatherEightAM"] == 0 and topCoverCodes["weatherElevenAM"] == 0 and topCoverCodes["weatherTwoPM"] == 1 and topCoverCodes["weatherFivePM"] == 1:
		print("In process, #3")
		if topCoverCodes["dayTime"] == 1:
			gap_day_time(3)
		elif topCoverCodes["dayTime"] == 0:		
			topCoverCodes["gapStart"] =  topCoverCodes["eightAMTimestamp"] + TENMINUTES
			topCoverCodes["gapEnd"] =  topCoverCodes["elevenAMTimestamp"] - TENMINUTES

	# 4
	elif topCoverCodes["weatherEightAM"] == 0 and topCoverCodes["weatherElevenAM"] == 1 and topCoverCodes["weatherTwoPM"] == 0 and topCoverCodes["weatherFivePM"] == 0:
		print("In process, #4")
		if topCoverCodes["dayTime"] == 1:
			gap_day_time(4)
		elif topCoverCodes["dayTime"] == 0:		
			topCoverCodes["gapStart"] =  topCoverCodes["twoPMTimestamp"] + TENMINUTES
			topCoverCodes["gapEnd"] =  topCoverCodes["fivePMTimestamp"] - TENMINUTES

	# 8
	elif topCoverCodes["weatherEightAM"] == 1 and topCoverCodes["weatherElevenAM"] == 0 and topCoverCodes["weatherTwoPM"] == 0 and topCoverCodes["weatherFivePM"] == 0:
		print("In process, #8")
		if topCoverCodes["dayTime"] == 1:
			gap_day_time(8)
		elif topCoverCodes["dayTime"] == 0:		
			topCoverCodes["gapStart"] =  topCoverCodes["elevenAMTimestamp"] + TENMINUTES
			topCoverCodes["gapEnd"] =  topCoverCodes["fivePMTimestamp"] - TENMINUTES

	# 12
	elif topCoverCodes["weatherEightAM"] == 1 and topCoverCodes["weatherElevenAM"] == 1 and topCoverCodes["weatherTwoPM"] == 0 and topCoverCodes["weatherFivePM"] == 0:
		print("In process, #12")
		if topCoverCodes["dayTime"] == 1:
			gap_day_time(12)
		elif topCoverCodes["dayTime"] == 0:		
			topCoverCodes["gapStart"] =  topCoverCodes["twoPMTimestamp"] + TENMINUTES
			topCoverCodes["gapEnd"] =  topCoverCodes["fivePMTimestamp"] - TENMINUTES

	print("TopCoverCodes = ", json.dumps(topCoverCodes, sort_keys=True, indent=4))
	### 2) Clear all values for next time to get processed. Only need to preserve gap times.
	resetCodesAndTimes(4)
	#print("In processForecastConditions topCoverCodes= ", topCoverCodes)	
	return

### Description: If forecast called during the day, this code sets up the time gaps to allow
###		the top cover to open.
### Flow: 		1) Get current time
###			2) Get timestamps at 8, 11, 2, 5
###			3) Set gap times based on truthTableVal
### Input: truthTableVal
### Output: none
### Example:
### 	Call this function from processForecastConditions() to set the gap times if doing so
###	during the daytime.
def gap_day_time(truthTableVal):
	""" This code set gaps times for tope cover when called during the day time. """
	
	# Get timestamp for current time
	timeString = datetime.datetime.now()											# Cali date and time datetime string
	timeFloat = datetime.datetime.timestamp(timeString)								# Convert to float time stamp
			
	# Eight AM
	eightAMString = str(datetime.date.today()) + ' 08:00:0'
	eightAM = datetime.datetime.strptime(eightAMString, "%Y-%m-%d %H:%M:%S").timestamp()	# float type
	# Eleven AM			
	elevenAMString = str(datetime.date.today()) + ' 11:00:0'
	elevenAM = datetime.datetime.strptime(elevenAMString, "%Y-%m-%d %H:%M:%S").timestamp()	# float type
	# Two PM		
	twoPMString = str(datetime.date.today()) + ' 14:00:0'
	twoPM = datetime.datetime.strptime(twoPMString, "%Y-%m-%d %H:%M:%S").timestamp()	# float type
	# Five PM			
	fivePMString = str(datetime.date.today()) + ' 17:00:0'
	fivePM = datetime.datetime.strptime(fivePMString, "%Y-%m-%d %H:%M:%S").timestamp()	# float type

	if truthTableVal == 0:
		if timefloat > eightAM and timefloat < elevenAM:
			topCoverCodes["gapStart"] =  topCoverCodes["elevenAMTimestamp"] + TENMINUTES
			topCoverCodes["gapEnd"] =  topCoverCodes["fivePMTimestamp"] - TENMINUTES
		elif timefloat > elevenAM and timefloat < twoPM:
			topCoverCodes["gapStart"] =  topCoverCodes["twoPMTimestamp"] + TENMINUTES
			topCoverCodes["gapEnd"] =  topCoverCodes["fivePMTimestamp"] - TENMINUTES
		elif timefloat > twoPM and timefloat < fivePM:
			topCoverCodes["gapStart"] = 0
			topCoverCodes["gapEnd"] = 0
			topCoverCodes["topCurrentStatus"] = 0
	elif truthTableVal == 1:
		if timefloat > eightAM and timefloat < elevenAM:
			topCoverCodes["gapStart"] =  topCoverCodes["elevenAMTimestamp"] + TENMINUTES
			topCoverCodes["gapEnd"] =  topCoverCodes["fivePMTimestamp"] - TENMINUTES
		else:
			topCoverCodes["gapStart"] = 0
			topCoverCodes["gapEnd"] = 0
			topCoverCodes["topCurrentStatus"] = 0
	elif truthTableVal == 2 or truthTableVal == 3 or truthTableVal == 4 or truthTableVal == 12:
		topCoverCodes["gapStart"] = 0
		topCoverCodes["gapEnd"] = 0
		topCoverCodes["topCurrentStatus"] = 0
	elif truthTableVal == 8:
		if timefloat > elevenAM and timefloat < twoPM:
			topCoverCodes["gapStart"] =  topCoverCodes["twoPMTimestamp"] + TENMINUTES
			topCoverCodes["gapEnd"] =  topCoverCodes["fivePMTimestamp"] - TENMINUTES
		else:
			topCoverCodes["gapStart"] = 0
			topCoverCodes["gapEnd"] = 0
			topCoverCodes["topCurrentStatus"] = 0

	return

### Description: Resets weather binary and timestamps to avoid incorrect truth table inputs on next interation of 
###		 acquiring the forecast
### Flow: 		1) Check what needs to be reset based on r and reset it
### Input: topCoverCodes, r 
### Output: none
### Example:
### 	Call this function from processForecastConditions() and fillTable() to clear used data
def resetCodesAndTimes(r):
	""" This code resets the codes for the truth table and dates and times for upcoming forecasts so will be restarted when forecast called again. """

	print("Inside RESET")

	### 1) Check what needs to be reset and reset it
	if r == 1:
		print("In reset, 1")
		topCoverCodes['weatherEightAM'] = 0
		topCoverCodes['eightAMTimestamp'] = 0.0
	elif r == 2:
		print("In reset, 2")
		topCoverCodes['weatherEightAM'] = 0
		topCoverCodes['weatherElevenAM'] = 0
		topCoverCodes['eightAMTimestamp'] = 0.0
		topCoverCodes['elevenAMTimestamp'] = 0.0
	elif r == 3:
		print("In reset, 3")
		topCoverCodes['weatherEightAM'] = 0
		topCoverCodes['weatherElevenAM'] = 0
		topCoverCodes['weatherTwoPM'] = 0
		topCoverCodes['eightAMTimestamp'] = 0.0
		topCoverCodes['elevenAMTimestamp'] = 0.0
		topCoverCodes['twoPMTimestamp'] = 0.0
	elif r == 4:
		print("In reset, 4")
		topCoverCodes['weatherEightAM'] = 0
		topCoverCodes['weatherElevenAM'] = 0
		topCoverCodes['weatherTwoPM'] = 0
		topCoverCodes['weatherFivePM'] = 0
		topCoverCodes['eightAMTimestamp'] = 0.0
		topCoverCodes['elevenAMTimestamp'] = 0.0
		topCoverCodes['twoPMTimestamp'] = 0.0
		topCoverCodes['fivePMTimestamp'] = 0.0

	return
	
################################

if __name__ == '__main__':
	getWeatherForTop()
	getForecastForTop()
	#getTopCoverStatus(topCoverCodes)
	#getTimeOfDay()
	#fillTable(topCoverCodes, jsonStringForecast, j)
	#processForecastConditions(topCoverCodes)


