#!/usr/bin/python3

import os               											# Allow interaction with operating system modules
import urllib.request											# urllib for python3, need to get url of OpenWeatherMap
															# https://docs.python.org/3/library/urllib.request.html#urllib.request.Request
import json													# Default data from API is in JSON format so need this module to parse it
															# https://docs.python.org/3/library/json.html?highlight=json#module-json
import datetime												# Used to get a human-readable timestamp
															# https://docs.python.org/3/library/datetime.html#module-datetime
from collections import OrderedDict								# Used to order the JSON data from the API in the same order it is imported as. Otherwise, output is unordered

#TODO add exception handling
#TODO: save top closing data to file/webpage, when and why it closed
#TODO: logic to account for sudden weather/forecast changes
#TODO Make input files to test all weather possibilities to see if desired result is achived

# Time Defines
oneHour = 3600.0									# Seconds
TENMINUTES = 600.0

topCoverCodes = {
				"status": 0,
				"dayTime": 0,
				"now": 0,
				"nextAPIPoint": 0,
				"eightAM": 0,
				"elevenAM": 0,
				"twoPM": 0,
				"fivePM": 0,
				"currentWeatherTime": 0.0,
				"eightAMTimestamp": 0.0,
				"elevenAMTimestamp": 0.0,
				"twoPMTimestamp": 0.0,
				"fivePMTimestamp": 0.0,
				"gapStart": 0.0,
				"gapEnd": 0.0
				}

### Request weather data (comes in JSON format) from OpenWeatherMap.com
zipCode = "90210"															# University of the Pacific zipcode = 95211
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

def getWeatherForTop(topCoverCodes):
	""" Returns curtent weather ID and time """
	
	print("In weather topCoverCodes= ", topCoverCodes)	
	# Get the API response of the current weather data
	url = weatherURL
	jsonStringWeather = requestAPI(url)

	# Parse the current weather data
	weatherID = jsonStringWeather['weather'][0]['id']
	weatherLocalTimeString = datetime.datetime.fromtimestamp(jsonStringWeather['dt'])	# Local time datetime.datetime type string
	weatherLocalTimestamp = datetime.datetime.strptime(str(weatherLocalTimeString), "%Y-%m-%d %H:%M:%S").timestamp()	# float type
	#print("Current ID: ", weatherID, "	Time: ", weatherLocalTimeString, "	Stamp: ", weatherLocalTimestamp)
	
	# Check ID against ID code file to see if bad weather
	if idCodeDictionary[weatherID] == 'x':
		#closeTopCoverCodes[1] = 1
		topCoverCodes['now'] = 1
		topCoverCodes['currentWeatherTime'] = weatherLocalTimestamp
		return topCoverCodes		
		#return closeTopCoverCodes
	return closeTopCoverCodes

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
	if topCoverCodes['dayTime'] == 0:							# Night time
		### Gather forecast for the day ahead starting at 8AM
		exitLoop = False
		j = 0		
		# Loop until 8AM then fill truth table for open top times
		while exitLoop == False:
			exitLoop = fillTable(topCoverCodes, jsonStringForecast, j)
			j = j + 1
		### Set gaps of time when good weather
		processForecastConditions(topCoverCodes)				
			
	elif topCoverCodes['dayTime'] == 1:							# Day time
		### Check weather now
		getWeatherForTop(topCoverCodes)
		if topCoverCodes['now'] == 1:
			topCoverCodes['status'] = 0	# close the top now if bad weather. TODO: Maybe hard code a 'close top' command to Arduino here or create an interrupt
		
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
	
	#if closeTopCoverCodes[0] == 0 and closeTopCoverCodes [5] != 0:

def getTimeOfDay(topCoverCodes):
	""" Sets time index to 1 if currently between 8:10am and 4:50pm when there is light. This allows top to open if during the day. """
	
	### Get todays 8AM and 4PM time stamp
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
	forecastLocalTimeString = str(datetime.datetime.fromtimestamp(jsonStringForecast['list'][j]['dt']))		# gives in local time
	if forecastLocalTimeString[11:] == "08:00:00":		
		### Get forecast between 8am - 5pm.
		# [j] = 8am, [j+1] = 11am, [j+2] = 2pm, [j+3] = 5pm
		# Fills truth table inputs
		
		if idCodeDictionary[jsonStringForecast['list'][j]['weather'][0]['id']] == 'x':
			topCoverCodes["eightAM"] = 1

		if idCodeDictionary[jsonStringForecast['list'][j+1]['weather'][0]['id']] == 'x':
			topCoverCodes["elevenAM"] = 1

		if idCodeDictionary[jsonStringForecast['list'][j+2]['weather'][0]['id']] == 'x':
			topCoverCodes["twoPM"] = 1	

		if idCodeDictionary[jsonStringForecast['list'][j+3]['weather'][0]['id']] == 'x':
			topCoverCodes["fivePM"] = 1

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
	### TODO: Make more if statements for datTime = 1, could be turned on at 9am so [0] = 11am, Also, maybe make the 4 if statements into a function	
	return False

def processForecastConditions(topCoverCodes):
	"""This function sets the times to allow the top cover to open based on when there is good weather in the daytime."""

	# bad weather == 1
	# Could have bad weather befre a 1 or after so only okay to open if 2 consecutive 0's 
	# 8AM | 11AM | 2PM | 5PM || Allow Open for that Day
	# ------------------------------------------------------------------------
# 0	#    0    |     0     |    0    |    0    || 	8:10am - 4:50pm
# 1	#    0    |     0     |    0    |    1    || 	8:10am - 1:50pm
# 2	#    0    |     0     |    1    |    0    || 	8:10am - 10:50am
# 3	#    0    |     0     |    1    |    1    || 	8:10am - 10:50am
# 4	#    0    |     1     |    0    |    0    || 	2:10pm - 4:50pm
	#    0    |     1     |    0    |    1    ||  		     0
	#    0    |     1     |    1    |    0    ||  		     0
	#    0    |     1     |    1    |    1    ||  		     0
# 8	#    1    |     0     |    0    |    0    || 	11:10am - 4:50pm
	#    1    |     0     |    0    |    1    ||  		     0
	#    1    |     0     |    1    |    0    ||  		     0
	#    1    |     0     |    1    |    1    ||  		     0
#12 #    1    |     1     |    0    |    0    || 	2:10pm - 4:50pm
	#    1    |     1     |    0    |    1    ||  		     0
	#    1    |     1     |    1    |    0    ||  		     0
	#    1    |     1     |    1    |    1    ||  		     0	
	
	# 0, truth table filled and all times filled by this point
	if topCoverCodes["eightAM"] == 0 and topCoverCodes["elevenAM"] == 0 and topCoverCodes["twoPM"] == 0 and topCoverCodes["fivePM"] == 0:
		# topCoverCodes["eightAMTimestamp"] =  topCoverCodes["eightAMTimestamp"] + TENMINUTES
		 #topCoverCodes["fivePMTimestamp"] =  topCoverCodes["fivePMTimestamp"] - TENMINUTES
		topCoverCodes["gapStart"] =  topCoverCodes["eightAMTimestamp"] + TENMINUTES
		topCoverCodes["gapEnd"] =  topCoverCodes["fivePMTimestamp"] - TENMINUTES

	# 1
	elif topCoverCodes["eightAM"] == 0 and topCoverCodes["elevenAM"] == 0 and topCoverCodes["twoPM"] == 0 and topCoverCodes["fivePM"] == 1:
		 topCoverCodes["gapStart"] =  topCoverCodes["eightAMTimestamp"] + TENMINUTES
		 topCoverCodes["gapEnd"] =  topCoverCodes["twoPMTimestamp"] - TENMINUTES
	
	# 2
	elif topCoverCodes["eightAM"] == 0 and topCoverCodes["elevenAM"] == 0 and topCoverCodes["twoPM"] == 1 and topCoverCodes["fivePM"] == 0:
		 topCoverCodes["gapStart"] =  topCoverCodes["eightAMTimestamp"] + TENMINUTES
		 topCoverCodes["gapEnd"] =  topCoverCodes["elevenAMTimestamp"] - TENMINUTES

	# 3
	elif topCoverCodes["eightAM"] == 0 and topCoverCodes["elevenAM"] == 0 and topCoverCodes["twoPM"] == 1 and topCoverCodes["fivePM"] == 1:
		 topCoverCodes["gapStart"] =  topCoverCodes["eightAMTimestamp"] + TENMINUTES
		 topCoverCodes["gapEnd"] =  topCoverCodes["elevenAMTimestamp"] - TENMINUTES

	# 4
	elif topCoverCodes["eightAM"] == 0 and topCoverCodes["elevenAM"] == 1 and topCoverCodes["twoPM"] == 0 and topCoverCodes["fivePM"] == 0:
		 topCoverCodes["gapStart"] =  topCoverCodes["twoPMTimestamp"] + TENMINUTES
		 topCoverCodes["gapEnd"] =  topCoverCodes["fivePMTimestamp"] - TENMINUTES

	# 8
	elif topCoverCodes["eightAM"] == 1 and topCoverCodes["elevenAM"] == 0 and topCoverCodes["twoPM"] == 0 and topCoverCodes["fivePM"] == 0:
		 topCoverCodes["gapStart"] =  topCoverCodes["elevenAMTimestamp"] + TENMINUTES
		 topCoverCodes["gapEnd"] =  topCoverCodes["fivePMTimestamp"] - TENMINUTES

	# 12
	elif topCoverCodes["eightAM"] == 1 and topCoverCodes["elevenAM"] == 1 and topCoverCodes["twoPM"] == 0 and topCoverCodes["fivePM"] == 0:
		 topCoverCodes["gapStart"] =  topCoverCodes["twoPMTimestamp"] + TENMINUTES
		 topCoverCodes["gapEnd"] =  topCoverCodes["fivePMTimestamp"] - TENMINUTES

	print("In processForecastConditions topCoverCodes= ", topCoverCodes)	
	return topCoverCodes
	
################################

if __name__ == '__main__':
	getWeatherForTop(topCoverCodes)
	getForecastForTop(topCoverCodes)
	getTopCoverStatus(topCoverCodes)
	getTimeOfDay(topCoverCodes)
	fillTable(topCoverCodes, jsonStringForecast, j)
	processForecastConditions(topCoverCodes)


