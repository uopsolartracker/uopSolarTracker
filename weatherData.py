#!/usr/bin/python3

import os               											# Allow interaction with operating system modules
import urllib.request											# urllib for python3, need to get url of OpenWeatherMap
															# https://docs.python.org/3/library/urllib.request.html#urllib.request.Request
import json													# Default data from API is in JSON format so need this module to parse it
															# https://docs.python.org/3/library/json.html?highlight=json#module-json
import datetime												# Used to get a human-readable timestamp
															# https://docs.python.org/3/library/datetime.html#module-datetime
from collections import OrderedDict								# Used to order the JSON data from the API in the same order it is imported as. Otherwise, output is unordered
import time
#import contextlib

#TODO add exception handling

# Time Defines
oneHour = 3600.0									# Seconds
closeTopCoverCodes = [0, 0, 0, 0, 0, 0, 0]					# List of state of the top cover of protection unit being closed and state of rain
													# FORMAT: closeTopCoverCodes = [close/open, Now, next API point, nextTime, +1h, 24h, +3h after 24h]
													#							  =  [	0	   ,	1  ,           2	      ,	       3	,   4   ,   5   ,   	     6  	   ]

	### Bad weather Truth Table ###
	# No bad weather = 0
	# Bad weather = 1
	# Now | NextAPIpoint | +1h | 24h | +3h || Allow Open for that Day
	# --------------------------------------------------------------------------------------
	#    0    |           0           |   0   |    0   |   0    ||        		1
	#    0    |           0           |   0   |    0   |   1    ||        		0
	#    0    |           0           |   0   |    1   |   X    ||        		0
	#    0    |           0           |   1   |    X   |   X    ||        		0
	#    0    |           1           |   X   |    X   |   X    ||        		0
	#    1    |           X           |   X   |    X   |   X    ||        		0

print("Declared = ", closeTopCoverCodes)
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
		closeTopCoverCodes[1] = 1
		return closeTopCoverCodes
	return closeTopCoverCodes

def getForecastForTop(closeTopCoverCodes):
	"""Returns a list of codes of weather to open the top cover of the protection unit or not"""

	print("In forecast = ", closeTopCoverCodes)

	### Timestamps
	time1 = datetime.datetime.utcnow()											# UTC time for timestamp
	utcStamp = datetime.datetime.timestamp(time1)
	californiaTime = datetime.datetime.now()									# Cali time for timestamp
	t1 = datetime.datetime.timestamp(californiaTime)							# use datetime to make a timestamp of previous timestamp into a float type
	#print("Local time = ", californiaTime)
	#print("UTC time = ", time1)
	#print("Local timestamp = ", t1)
	#print("UTC timestamp = ", utcStamp)
		
	# Get the API response of the forecast data
	url = forecastURL
	jsonStringForecast = requestAPI(url)

	################# Parse the JSON strings for ID and time ################# 
	#################									#################

	# Parse the forecast data into a list	
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

	#TODO: Capture weather/forecast data every ten minutes up to three hours. close if raining during that time. open if no rain for 1 hour after rain stops and no rain for three hours
	### Check if is raining or might rain
	nextAPIPoint = forecastID[0]

	outFile = open('Close_Top_Logs.txt', 'a')									# Open file to prepare for write

	### Check if bad weather at next API forecast capture point
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
	
	
################################

if __name__ == '__main__':
	getWeatherForTop(closeTopCoverCodes)
	getForecastForTop(closeTopCoverCodes)


