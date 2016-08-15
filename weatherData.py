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

# Time Defines
oneHour = 3600.0									# Seconds
#eightAM = 
closeTopCoverCodes = [0, 0, 0, 0, 0, 0, 0]					# List of state of the top cover of protection unit being closed and state of rain
													# FORMAT: closeTopCoverCodes = [closed/open, now, next API point, 24h, 24h + 3h, time, nextTime, ]
													#							  =  [      	   0	     ,   1   ,           2	        ,    3  ,        4      ,   5    ,        6        ]
													# [0] closed/open	: Status of top cover. Also gets set to send command to open or close the top
													# 				: 0 = closed
													# 				: 1 = open
													# [1] now		: Status of current weather (Ask yourself, is there bad weather?)
													# 				: 0 = no, not bad weather
													# 				: 1 = yes, bad weather
													# [2] next API Point : Status of forecast of next closest API forecast capture point. The API gives forecasts
													#			  	    in 3 hour increments starting at 2AM PST (12AM UTC).
													#				    EXAMPLE: If get forecast data from API at 3:23AM, the next closest forecast time given
													#				    by the API is 5AM (3 hours from 2AM). 
													# 				: 0 = not bad weather
													# 				: 1 = bad weather
													# [3] 24h		: Status of forecast 24 hours from now
													# 				: 0 = not bad weather
													# 				: 1 = bad weather
													# [4] 24h + 3h 	: Status of forecast 24 hours + next API point past 24 hours. Might not be raining 24h from
													#				  now but may be raining 24h + 1 minute from now. So dont want top to open then start raining.
													# 				: 0 = not bad weather
													# 				: 1 = bad weather
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
				}

	### Bad weather Truth Table ###
	# No bad weather = 0
	# Bad weather = 1
	# closed/opened | Now | NextAPIpoint | +1h | 24h | +3h || Allow Open for that Day
	# --------------------------------------------------------------------------------------
	#    0    |           0           |   0   |    0   |   0    ||        		1
	#    0    |           0           |   0   |    0   |   1    ||        		0
	#    0    |           0           |   0   |    1   |   X    ||        		0
	#    0    |           0           |   1   |    X   |   X    ||        		0
	#    0    |           1           |   X   |    X   |   X    ||        		0
	#    1    |           X           |   X   |    X   |   X    ||        		0

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

#example http://api.openweathermap.org/data/2.5/weather?q=65065us&APPID=849eb6e48e5b5e037e1cb47efea60d62

def requestAPI(url):
	""" Request and read the API page """

	# urlopen returns a bytes object so decode it so it can be read by the JSON module
	#apiResponseForecast = urllib.request.urlopen(forecastURL).read().decode('utf-8')
	#apiResponseWeather = urllib.request.urlopen(weatherURL).read().decode('utf-8')
	#TODO: Close the URL with .close()

	# urlopen returns a bytes object so decode it so it can be read by the JSON module
	apiResponse = urllib.request.urlopen(url).read().decode('utf-8')
	#TODO: Close the URL with .close()
	# Deserialize the JSON data to a string
	jsonString = json.loads(apiResponse, object_pairs_hook=OrderedDict)

	# Deserialize the JSON data to a string
	#jsonStringForecast = json.loads(apiResponseForecast, object_pairs_hook=OrderedDict)
	#jsonStringWeather = json.loads(apiResponseWeather, object_pairs_hook=OrderedDict)

	return jsonString

def getWeatherForTop(closeTopCoverCodes):
	""" Returns curtent weather ID and time """
	
	print("In weather = ", closeTopCoverCodes)	
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

def getForecastForTop(closeTopCoverCodes):
	"""Returns a list of codes of weather to open the top cover of the protection unit or not"""

	### Get the API response of the forecast data
	url = forecastURL
	jsonStringForecast = requestAPI(url)

	### Parse the forecast data into a lists
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

	### 1) Check if night or day ( day = anytime between 8:10am and 4:50pm)
	getTimeOfDay(topCoverCodes)
	### 2) 
	if topCoverCodes['dayTime'] == 0:							# Night time
		### Gather forecast for the day ahead starting at 8AM		
		#nextAPIPoint = jsonStringForecast['list'][0]['weather'][0]['id']
		x = True
		j = 0		
		while x == True:		
			forecastLocalTimeString = str(datetime.datetime.fromtimestamp(jsonStringForecast['list'][j]['dt']))		# gives in local time
			if forecastLocalTimeString[11:] == "08:00:00":		
				### Get forecast between 8am - 5pm. TODO: Make function for the 4 if statements?
				# [j] = 8am, [j+1] = 11am, [j+2] = 2pm, [j+3] = 5pm
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
				
		########### LEFT OFF HERE, WORKING ON processForecastConditions FUNCTION
				### Set gaps of time when good weather
				processForecastConditions(topCoverCodes)
				# -> ... follow notebook code ...
				x = False	

			j = j + 1
			# Next convert the local time string to a local time timstamp
			#forecastLocalTimestamp = datetime.datetime.strptime(str(forecastLocalTimeString), "%Y-%m-%d %H:%M:%S").timestamp()
			
	elif topCoverCodes['dayTime'] == 1:							# Day time
		print("place holder")

		############################ ERROR CHECKING AND CONVERSION TESTING ############################
		
		#time1 = datetime.datetime.utcnow()											# UTC time for timestamp in readable format
		#utcStamp = datetime.datetime.timestamp(time1)								# gives a float
		#californiaTime = datetime.datetime.now()									# Cali time for timestamp
		#t1 = datetime.datetime.timestamp(californiaTime)							# float type
		#print("	Local time now= ", californiaTime)
		#print("UTC time = ", time1)
		#print("Local timestamp = ", t1)
		#print("UTC timestamp = ", utcStamp)		

		#localTime = datetime.datetime.fromtimestamp(jsonStringForecast['list'][i]['dt'])
		#print("Forecast Local Text = ", localTime)
		#print("Forecast UTC Text = ", datetime.datetime.utcfromtimestamp(jsonStringForecast['list'][i]['dt']))

		#a = datetime.datetime.strptime(str(localTime), "%Y-%m-%d %H:%M:%S").timestamp()
		#print('Forecast Local time as timestamp = ', a)
		#print('Forecast UTC as timestamp = ', forecastTime[i])
		#b = datetime.datetime.fromtimestamp(a)
		#print("Forcast Local time back to text = ", b)
		#print("Forecast UTC time back to text = ", datetime.datetime.utcfromtimestamp(forecastTime[i]))

		###########################################################################################
	

	#time1 = datetime.datetime.now()											# UTC time for timestamp in readable format
	#time1Float = datetime.datetime.timestamp(time1)								# gives a float
	#time.sleep(2)
	#time2 = datetime.datetime.now()									# Cali time for timestamp
	#time2Float = datetime.datetime.timestamp(time2)							# float type
	#print("Time difference = ", time2Float - time1Float)	
	#print(weatherLocalTimestamp - forecastTime[6])
	#print(forecastTime[3] - forecastTime[2])
		
	############################ ERROR CHECKING AND CONVERSION TESTING ############################
	
	#print("Weather time UTC timestamp = ", weatherTime)
	#weatherUTCStamp = datetime.datetime.utcfromtimestamp(weatherTime)
	#print("Text Weather UTC =", weatherUTCStamp)
	#lt = datetime.datetime.fromtimestamp(weatherTime)
	#print("Text Weather Now = ", lt)
	#c = datetime.datetime.strptime(str(lt), "%Y-%m-%d %H:%M:%S").timestamp()
	#print("Weather time Now timestamp = ", c)
	#weatherUTCtxt = jsonStringWeather['dt_txt']
	#print("Weather UTC Text = ", weatherUTCtxt)
	#print("Timestamp now = ", datetime.datetime.strptime(str(weatherUTCStamp), "%Y-%m-%d %H:%M:%S").timestamp())
	#print("Time Text Now = ", )
			
	###########################################################################################

	#outFile = open('Close_Top_Logs.txt', 'a')									# Open file to prepare for write




#################################################################################################
	####### OLD LOGIC
	nextAPIPoint = forecastID[0]											# First index is next API capture point of forecast
	if idCodeDictionary[nextAPIPoint] == 'x':									# If weather in 3 hours or now is raining, close the top of protection unit
		closeTopCoverCodes[2] = 1
	else:
		closeTopCoverCodes[3] = forecastTime[0] + oneHour					# Save time to check if still not bad weather

		#captureTime = datetime.datetime.fromtimestamp(forecastTime[i])		# Get time of projected forecast
		#forecastDescription = descriptionCodeDictionary[forecastID[i]]			# Get reason for closing top from the code dictionary
		#outFile.write(captureTime, "	", forecastDescription)					# Write to file
		#outFile.close()													# Close file
		#print("Id codeDict = ", idCodeDictionary[forecastID[0]], "	", descriptionCodeDictionary[forecastID[0]])
		#print("ForecastID: ", forecastID[0])
		#print("WeatherDict = ",  idCodeDictionary[weatherID])
		#print("WeatherID: ", weatherID)

	### Check if bad weather in next 24 hours
	for j in range(1, 9):								# Start at 2nd index, this is three hours past first API point, each index is 3 hours ahead
		if idCodeDictionary[forecastID[j]] == 'x':			# 24 hours is 8 indicies,
			closeTopCoverCodes[5] = 1

	### Check if bad weather 3 hours after 24h
	if idCodeDictionary[forecastID[9]] == 'x':
			closeTopCoverCodes[6] = 1

	return closeTopCoverCodes
######################################################################################################


def getTopCoverStatus(closeTopCoverCodes):
	""" Sets open/close index based on other closeTopCoverCodes indicies and returns closeTopCoverCodes to the main function """
	
	#if closeTopCoverCodes[0] == 0 and closeTopCoverCodes [5] != 0:

def getTimeOfDay(topCoverCodes):
	""" Sets time index to 1 if between 8am and 4pm when there is light. This allows top to open if during the day. """
	
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
	
	# 0
	if topCoverCodes["eightAM"] == 0 and topCoverCodes["elevenAM"] == 0 and topCoverCodes["twoPM"] == 0 and topCoverCodes["fivePM"] == 0:
		print("PLACE HOLDER")
		# grab date from dt, 
		# grab time from dt
		# add ten min or subtract ten min from time
		# concat with date to give a date and time when to actually start to open top
		# save to topCoverCodes
		# return?
	# 1
	elif topCoverCodes["eightAM"] == 0 and topCoverCodes["elevenAM"] == 0 and topCoverCodes["twoPM"] == 0 and topCoverCodes["fivePM"] == 1:
		print("PLACE HOLDER")
	# 2
	elif topCoverCodes["eightAM"] == 0 and topCoverCodes["elevenAM"] == 0 and topCoverCodes["twoPM"] == 1 and topCoverCodes["fivePM"] == 0:
		print("PLACE HOLDER")
	# 3
	elif topCoverCodes["eightAM"] == 0 and topCoverCodes["elevenAM"] == 0 and topCoverCodes["twoPM"] == 1 and topCoverCodes["fivePM"] == 1:
		print("PLACE HOLDER")
	# 4
	elif topCoverCodes["eightAM"] == 0 and topCoverCodes["elevenAM"] == 1 and topCoverCodes["twoPM"] == 0 and topCoverCodes["fivePM"] == 0:
		print("PLACE HOLDER")
	# 8
	elif topCoverCodes["eightAM"] == 1 and topCoverCodes["elevenAM"] == 0 and topCoverCodes["twoPM"] == 0 and topCoverCodes["fivePM"] == 0:
		print("PLACE HOLDER")
	# 12
	elif topCoverCodes["eightAM"] == 1 and topCoverCodes["elevenAM"] == 1 and topCoverCodes["twoPM"] == 0 and topCoverCodes["fivePM"] == 0:
		print("PLACE HOLDER")

	return topCoverCodes
	
################################

if __name__ == '__main__':
	getWeatherForTop(closeTopCoverCodes)
	getForecastForTop(closeTopCoverCodes)


