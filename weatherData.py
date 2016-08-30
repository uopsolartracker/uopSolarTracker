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
#TODO: add descr to all funcitons
#TODO: save top closing data to file/webpage, when and why it closed
#TODO: logic to account for sudden weather/forecast changes
#TODO: Make input files to test all weather possibilities to see if desired result is achived
#TODO: Delete all uneccassary returns of topCoverCodes that return to a funciton in this file, only have returns to save to calling file

# Time Defines (seconds)
TENMINUTES = 600.0

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

print("Init topCoverCodes = ", topCoverCodes)

#example http://api.openweathermap.org/data/2.5/weather?q=65065us&APPID=849eb6e48e5b5e037e1cb47efea60d62

### Description: Gets current weather and sets badWeatherNow attribute. Is to be called from main.
### Flow: 	--> Calls forecast API 
###		--> Parses incoming JSON 
###		--> Converts times to local time
###		--> Checks API weather code against code in idCodeDictionary to see if bad weather
###		--> Sets bad weather indicator by setting topCoverCodes['badWeatherNow'] = 1 and saves time
### Input: topCoverCodes
### Output: topCoverCodes
### Example:
### 	Call getWeatherForTop() from main --> sets topCoverCodes.topCurrentStatus = 0 (good weather) or 1 (bad weather)
def getWeatherForTop(topCoverCodes):
	""" Sets current weather ID and time """
	
	print("In weather topCoverCodes= ", topCoverCodes)	
	# Get the API response of the current weather data
	url = weatherURL
	jsonStringWeather = requestAPI(url)

	# Parse the current weather data
	weatherID = jsonStringWeather['weather'][0]['id']
	weatherLocalTimeString = datetime.datetime.fromtimestamp(jsonStringWeather['dt'])	# Local time datetime.datetime type string
	weatherLocalTimestamp = datetime.datetime.strptime(str(weatherLocalTimeString), "%Y-%m-%d %H:%M:%S").timestamp()	# float type
	#print("Current ID: ", weatherID, "	Time: ", weatherLocalTimeString, "	Stamp: ", weatherLocalTimestamp)
	
	# Check ID against ID code file to see if bad weather, x = bad weather in text file
	if idCodeDictionary[weatherID] == 'x':
		topCoverCodes['badWeatherNow'] = 1
		topCoverCodes['currentWeatherTime'] = weatherLocalTimestamp
		return topCoverCodes		
	return topCoverCodes

### Description: Gets current forecast and sets badWeatherNow attribute. Is to be called from main.
### Flow: 	--> Calls forecast API 
### Input: topCoverCodes
### Output: topCoverCodes
### Example:
### 	Call getWeatherForTop() from main --> 
def getForecastForTop(topCoverCodes):
	"""Returns a list of codes of weather to open the top cover of the protection unit or not"""
	
	print("In weather topCoverCodes= ", topCoverCodes)	
	
	### Get the API response of the forecast data
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

	### 1) Check if night or day ( day = anytime between 8:10am and 4:50pm), sets ['dayTime'] = 1/0
	getTimeOfDay(topCoverCodes)
	### 2) 
	### Night time
	if topCoverCodes['dayTime'] == 0:
		findOpenTimes(topCoverCodes, jsonStringForecast)			
		return topCoverCodes
	### Day time
	elif topCoverCodes['dayTime'] == 1:
		### Check weather now
		getWeatherForTop(topCoverCodes)
		if topCoverCodes['badWeatherNow'] == 1:
			topCoverCodes['topCurrentStatus'] = 0	# close the top now if bad weather. TODO: Maybe hard code a 'close top' command to Arduino here or create an interrupt
		findOpenTimes(topCoverCodes, jsonStringForecast)			
		return topCoverCodes
	
	#outFile = open('Close_Top_Logs.txt', 'a')									# Open file to prepare for write

def requestAPI(url):
	""" Request and read the API page """

	# urlopen returns a bytes object so decode it so it can be read by the JSON module
	apiResponse = urllib.request.urlopen(url).read().decode('utf-8')
	#TODO: Close the URL with .close()
	# Deserialize the JSON data to a string
	jsonString = json.loads(apiResponse, object_pairs_hook=OrderedDict)

	return jsonString

def getTopCoverStatus(topCoverCodes):
	""" Sets open/close index based on other closeTopCoverCodes indicies and returns closeTopCoverCodes to the main function """

def findOpenTimes(TopCoverCodes, jsonStringForecast):
	""" Top Level to find times to allow th top cover to open """

	### Gather forecast for the day ahead starting at 8AM
	exitLoop = False
	j = 0		
	# Loop until day time then fill truth table for open top times
	while exitLoop == False:
		exitLoop = fillTable(topCoverCodes, jsonStringForecast, j)
		j = j + 1
	### Set gaps of time when good weather
	processForecastConditions(topCoverCodes)	
	
	return

def getTimeOfDay(topCoverCodes):
	""" Sets time index to 1 if currently between 8:10am and 4:50pm when there is light. This allows top to open if during the day. """
	
	### Get todays 8:10AM and 4:50PM time stamp
	eightTenAMString = str(datetime.date.today()) + ' 08:10:0'
	eightTenAM = datetime.datetime.strptime(eightTenAMString, "%Y-%m-%d %H:%M:%S").timestamp()	# float type
	fourFiftyPMString = str(datetime.date.today()) + ' 16:50:0'
	fourFiftyPM = datetime.datetime.strptime(fourFiftyPMString, "%Y-%m-%d %H:%M:%S").timestamp()	# float type

	### Get time stamp for current time
	timeString = datetime.datetime.now()											# Cali date and time datetime string
	timeFloat = datetime.datetime.timestamp(timeString)								# Convert to float time stamp

	### Set index if during day
	if timeFloat >= eightTenAM and timeFloat <= fourFiftyPM:
		topCoverCodes['dayTime'] = 1
		return topCoverCodes
	topCoverCodes['dayTime'] = 0
	
	return topCoverCodes

def fillTable(topCoverCodes, jsonStringForecast, j):
	""" Saves time of day to open top and sets up truth table for when there is bad weather. """ 

	###TODO: Maybe make a function for the code below.
	forecastLocalTimeString = str(datetime.datetime.fromtimestamp(jsonStringForecast['list'][j]['dt']))		# gives in local time
	if forecastLocalTimeString[11:] == "08:00:00":		
		### Get forecast between 8am - 5pm.
		# [j] = 8am, [j+1] = 11am, [j+2] = 2pm, [j+3] = 5pm
		# Fills truth table inputs, x = bad weather
		
		if idCodeDictionary[jsonStringForecast['list'][j]['weather'][0]['id']] == 'x':
			topCoverCodes["weatherEightAM"] = 1

		if idCodeDictionary[jsonStringForecast['list'][j+1]['weather'][0]['id']] == 'x':
			topCoverCodes["weatherElevenAM"] = 1

		if idCodeDictionary[jsonStringForecast['list'][j+2]['weather'][0]['id']] == 'x':
			topCoverCodes["weatherTwoPM"] = 1	

		if idCodeDictionary[jsonStringForecast['list'][j+3]['weather'][0]['id']] == 'x':
			topCoverCodes["weatherFivePM"] = 1

		### Fill 8-5 timestamps with real times. Convert and save the times
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

		print("In fillTable topCoverCodes= ", topCoverCodes)	
		return True
	elif forecastLocalTimeString[11:] == "11:00:00":		
		### Get forecast between 11am - 5pm.
		# [j] = 11am, [j+1] = 2pm, [j+2] = 5pm
		# Fills truth table inputs
		
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
		
		### Set other values to 0 so that combination will get processed correctly
		resetCodesAndTimes(topCoverCodes, 1)

		print("In fillTable topCoverCodes= ", topCoverCodes)	
		return True
	elif forecastLocalTimeString[11:] == "14:00:00":		
		### Get forecast between 2pm - 5pm.
		# [j] = 2pm, [j+1] = 5pm
		# Fills truth table inputs
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
		
		### Set other values to 0 so that combination will get processed correctly
		resetCodesAndTimes(topCoverCodes, 2)

		print("In fillTable topCoverCodes= ", topCoverCodes)	
		return True
	elif forecastLocalTimeString[11:] == "17:00:00":		
		### Get forecast at 5pm.
		# [j] = 5pm
		# Fills truth table inputs
		if idCodeDictionary[jsonStringForecast['list'][j]['weather'][0]['id']] == 'x':
			topCoverCodes["weatherFivePM"] = 1
		
		### Fill 5pm timestamp with real times. Convert and save the time
		# 5PM				
		forecastLocalTimeString = datetime.datetime.fromtimestamp(jsonStringForecast['list'][j+1]['dt'])
		topCoverCodes["fivePMTimestamp"] = datetime.datetime.strptime(str(forecastLocalTimeString), "%Y-%m-%d %H:%M:%S").timestamp()
		
		### Set other values to 0 so that combination will get processed correctly
		resetCodesAndTimes(topCoverCodes, 3)

		print("In fillTable topCoverCodes= ", topCoverCodes)	
		return True
	return False

def processForecastConditions(topCoverCodes):
	"""This function sets the time period to allow the top cover to open based on when there is good weather in the daytime."""

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
	
	# 0, truth table filled and all times filled by this point
	if topCoverCodes["weatherEightAM"] == 0 and topCoverCodes["weatherElevenAM"] == 0 and topCoverCodes["weatherTwoPM"] == 0 and topCoverCodes["weatherFivePM"] == 0:
		# topCoverCodes["eightAMTimestamp"] =  topCoverCodes["eightAMTimestamp"] + TENMINUTES
		 #topCoverCodes["fivePMTimestamp"] =  topCoverCodes["fivePMTimestamp"] - TENMINUTES
		topCoverCodes["gapStart"] =  topCoverCodes["eightAMTimestamp"] + TENMINUTES
		topCoverCodes["gapEnd"] =  topCoverCodes["fivePMTimestamp"] - TENMINUTES

	# 1
	elif topCoverCodes["weatherEightAM"] == 0 and topCoverCodes["weatherElevenAM"] == 0 and topCoverCodes["weatherTwoPM"] == 0 and topCoverCodes["weatherFivePM"] == 1:
		 topCoverCodes["gapStart"] =  topCoverCodes["eightAMTimestamp"] + TENMINUTES
		 topCoverCodes["gapEnd"] =  topCoverCodes["twoPMTimestamp"] - TENMINUTES
	
	# 2
	elif topCoverCodes["weatherEightAM"] == 0 and topCoverCodes["weatherElevenAM"] == 0 and topCoverCodes["weatherTwoPM"] == 1 and topCoverCodes["weatherFivePM"] == 0:
		 topCoverCodes["gapStart"] =  topCoverCodes["eightAMTimestamp"] + TENMINUTES
		 topCoverCodes["gapEnd"] =  topCoverCodes["elevenAMTimestamp"] - TENMINUTES

	# 3
	elif topCoverCodes["weatherEightAM"] == 0 and topCoverCodes["weatherElevenAM"] == 0 and topCoverCodes["weatherTwoPM"] == 1 and topCoverCodes["weatherFivePM"] == 1:
		 topCoverCodes["gapStart"] =  topCoverCodes["eightAMTimestamp"] + TENMINUTES
		 topCoverCodes["gapEnd"] =  topCoverCodes["elevenAMTimestamp"] - TENMINUTES

	# 4
	elif topCoverCodes["weatherEightAM"] == 0 and topCoverCodes["weatherElevenAM"] == 1 and topCoverCodes["weatherTwoPM"] == 0 and topCoverCodes["weatherFivePM"] == 0:
		 topCoverCodes["gapStart"] =  topCoverCodes["twoPMTimestamp"] + TENMINUTES
		 topCoverCodes["gapEnd"] =  topCoverCodes["fivePMTimestamp"] - TENMINUTES

	# 8
	elif topCoverCodes["weatherEightAM"] == 1 and topCoverCodes["weatherElevenAM"] == 0 and topCoverCodes["weatherTwoPM"] == 0 and topCoverCodes["weatherFivePM"] == 0:
		 topCoverCodes["gapStart"] =  topCoverCodes["elevenAMTimestamp"] + TENMINUTES
		 topCoverCodes["gapEnd"] =  topCoverCodes["fivePMTimestamp"] - TENMINUTES

	# 12
	elif topCoverCodes["weatherEightAM"] == 1 and topCoverCodes["weatherElevenAM"] == 1 and topCoverCodes["weatherTwoPM"] == 0 and topCoverCodes["weatherFivePM"] == 0:
		 topCoverCodes["gapStart"] =  topCoverCodes["twoPMTimestamp"] + TENMINUTES
		 topCoverCodes["gapEnd"] =  topCoverCodes["fivePMTimestamp"] - TENMINUTES

	### Clear all values for next time to get processed
	resetCodesAndTimes(topCoverCodes, 4)
	print("In processForecastConditions topCoverCodes= ", topCoverCodes)	
	return topCoverCodes

def resetCodesAndTimes(topCoverCodes, r):
	""" This code resets the codes for the truth table and dates and times for upcoming forecasts so will be restarted when forecast called again. """

	print("In RESET")
	if r == 1:
		topCoverCodes['weatherEightAM'] = 0
		topCoverCodes['eightAMTimestamp'] = 0.0
	elif r == 2:
		topCoverCodes['weatherEightAM'] = 0
		topCoverCodes['weatherElevenAM'] = 0
		topCoverCodes['eightAMTimestamp'] = 0.0
		topCoverCodes['elevenAMTimestamp'] = 0.0
	elif r == 3:
		topCoverCodes['weatherEightAM'] = 0
		topCoverCodes['weatherElevenAM'] = 0
		topCoverCodes['weatherTwoPM'] = 0
		topCoverCodes['eightAMTimestamp'] = 0.0
		topCoverCodes['elevenAMTimestamp'] = 0.0
		topCoverCodes['twoPMTimestamp'] = 0.0
	elif r == 4:
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
	getWeatherForTop(topCoverCodes)
	getForecastForTop(topCoverCodes)
	getTopCoverStatus(topCoverCodes)
	getTimeOfDay(topCoverCodes)
	fillTable(topCoverCodes, jsonStringForecast, j)
	processForecastConditions(topCoverCodes)


