#!/usr/bin/python3

import os               											# Allow interaction with operating system modules
import urllib.request											# urllib for python3, need to get url of OpenWeatherMap
															# https://docs.python.org/3/library/urllib.request.html#urllib.request.Request
import json													# Default data from API is in JSON format so need this module to parse it
															# https://docs.python.org/3/library/json.html?highlight=json#module-json
#import time													# Used to get a current timestamp
import datetime												# Used to get a human-readable timestamp
															# https://docs.python.org/3/library/datetime.html#module-datetime
from collections import OrderedDict								# Used to order the JSON data from the API in the same order it is imported as. Otherwise, output is unordered

### Request weather data (JSON) from OpenWeatherMap.com
urlBase = "http://api.openweathermap.org/data/2.5/forecast?q="
zipCode = "90210"											# University of the Pacific zipcode = 95211
APIKey = "849eb6e48e5b5e037e1cb47efea60d62"
url = urlBase + zipCode + ",us&APPID=" + APIKey					# URL of OpenWeatherMap API

#example http://api.openweathermap.org/data/2.5/weather?q=65065us&APPID=849eb6e48e5b5e037e1cb47efea60d62

api_response = urllib.request.urlopen(url).read().decode('utf-8')		# Request and read the API page. 
															# urlopen returns a bytes object so decode it so it can be read by the JSON module
#TODO: Close the URL with .close()

### Timestamps
time1 = datetime.datetime.utcnow()								# UTC time for timestamp
t1 = datetime.datetime.timestamp(time1)						# use datetime to make a timestamp of previous timestamp into a float type
californiaTime = datetime.datetime.now()						# Cali time for timestamp
print("TIME = ", californiaTime)

### Parse the JSON data
json_string = json.loads(api_response, object_pairs_hook=OrderedDict)			# Deserialize the data to string
#print("LOADED = ", json_string, "		")

#json_formatted_str = json.dumps(json_string, indent=4)
#print("Output = ", json_formatted_str)
##print("Weather ID = ", json_string['list'][0]['weather'][0]['id'])
# TODO: make a loop to loop over however many weather ID's there are. we are using about 40 but make it work for any value
weatherID = [ ]
forecastTime = [ ]
for i in range(39):
	weatherID.append(json_string['list'][i]['weather'][0]['id'])			# Create a list of forecasted weather ID's
	forecastTime.append(json_string['list'][i]['dt'])					# Create a list of forecast time data, API gives time in UTC (unix)
	print("i = ", i, " WeatherID = ", weatherID[i])
	print("i = ", i, " Time = ", forecastTime[i])

### Check if is raining or might rain
# Read in txt file into a python dictionary
codeDictionary = {}
with open('weatherCodes.txt', 'r') as weatherCodes:
	skipFirstLine = next(weatherCodes)
	for line in weatherCodes:
		splitLine = line.split()
		#codeDictionary[int(splitLine[0])] = ", ".join(splitLine[1:])	# Capture description
		codeDictionary[int(splitLine[0])] = ", ".join(splitLine[1])		# Do not capture description
if codeDictionary[weatherID[0]] == '-':							# If weather in 3 hours is raining, close the top of protection unit
	print("win")




### Save weather data to a file, save only if had to close top and time and why
# Keep data for only 1 week?

### Send command to Arduino to close top cover?

