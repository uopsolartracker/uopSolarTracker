#!/usr/bin/python3

import os               											# Allow interaction with operating system modules
import urllib.request											# urllib for python3, need to get url of OpenWeatherMap
															# https://docs.python.org/3/library/urllib.request.html#urllib.request.Request
import json													# Default data from API is in JSON format so need this module to parse it
															# https://docs.python.org/3/library/json.html?highlight=json#module-json
import datetime												# Used to get a human-readable timestamp
															# https://docs.python.org/3/library/datetime.html#module-datetime
from collections import OrderedDict								# Used to order the JSON data from the API in the same order it is imported as. Otherwise, output is unordered
#import contextlib

#TODO add exception handling

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

def getWeather():
	### Timestamps
	time1 = datetime.datetime.utcnow()											# UTC time for timestamp
	t1 = datetime.datetime.timestamp(time1)									# use datetime to make a timestamp of previous timestamp into a float type
	californiaTime = datetime.datetime.now()									# Cali time for timestamp
	#print("TIME = ", californiaTime)
	
	### Request and read the API page
	# urlopen returns a bytes object so decode it so it can be read by the JSON module
	apiResponseForecast = urllib.request.urlopen(forecastURL).read().decode('utf-8')
	apiResponseWeather = urllib.request.urlopen(weatherURL).read().decode('utf-8')
	#TODO: Close the URL with .close()

	### Deserialize the JSON data to a string
	jsonStringForecast = json.loads(apiResponseForecast, object_pairs_hook=OrderedDict)
	jsonStringWeather = json.loads(apiResponseWeather, object_pairs_hook=OrderedDict)

	### Parse the JSON strings for ID and time
	# Parse the forecast data into a list	
	forecastID = [ ]
	forecastTime = [ ]
	for i in range(jsonStringForecast['cnt']):									# 'cnt' is the count of lines returned by the API
		forecastID.append(jsonStringForecast['list'][i]['weather'][0]['id'])			# Create a list of forecasted weather ID's
		forecastTime.append(jsonStringForecast['list'][i]['dt'])					# Create a list of forecast time data, API gives time in UTC (unix)
		#print("i = ", i, " WeatherID = ", weatherID[i])
		#print("i = ", i, " Time = ", forecastTime[i])	


		tt = datetime.datetime(jsonStringForecast['dt_txt'])


		print(tt)
	# Parse the current weather data
	weatherID = jsonStringWeather['weather'][0]['id']
	weatherTime = jsonStringWeather['dt']

	#TODO: Make sure all times are local times
	#TODO: Capture weather/forecast data every ten minutes up to three hours. close if raining during that time. open if no rain for 1 hour after rain stops and no rain for three hours
	### Check if is raining or might rain
	outFile = open('Close_Top_Logs.txt', 'a')									# Open file to prepare for write
	#for i in range(jsonStringForecast['cnt']):									# Use the for loop if want forcast for more than three hours ahead, each iteration is 3 hours more
	if idCodeDictionary[forecastID[0]] == 'x' or idCodeDictionary[weatherID] == 'x':	# If weather in 3 hours or now is raining, close the top of protection unit
		#captureTime = datetime.datetime.fromtimestamp(forecastTime[i])		# Get time of projected forecast
		#forecastDescription = descriptionCodeDictionary[forecastID[i]]			# Get reason for closing top from the code dictionary
		#outFile.write(captureTime, "	", forecastDescription)					# Write to file
		#outFile.close()													# Close file
		print("Id codeDict = ", idCodeDictionary[forecastID[0]], "	", descriptionCodeDictionary[forecastID[0]])
		print("ForecastID: ", forecastID[0])
		print("WeatherDict = ",  idCodeDictionary[weatherID])
		print("WeatherID: ", weatherID)
		return 1
	return 0
	
######

if __name__ == '__main__':
	getWeather()



