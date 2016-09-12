#!/usr/bin/python3

import sys
import datetime
import weatherDataTESTER
import json

### Test Cases for WeatherData.py
TENMIN = 600.0

print("Begin test......................................................................")
print(" ")
print("IN TESTER......................")
#print("Tester weatherData = ", weatherDataTester.topCoverCodes)
print(" ")

### Read in text file of weather codes into a python dictionary
idCodeList = [ ]
with open('weatherCodes.txt', 'r') as weatherCodes:
	skipFirstLine = next(weatherCodes)						# Skip first line of text file
	for line in weatherCodes:
		splitLine = line.split()
		idCodeList.append(int(splitLine[0]))						# Capture ID only




	### argv[2] == 05:22:00 (some specific time to simulate the call time to getForecastForTop()
	#timeStrNight = str(datetime.date.today()) + ' ' + argv[2]
	#timeStampNight = datetime.datetime.strptime(timeStrNight, "%Y-%m-%d %H:%M:%S").timestamp()	# float type, pass to getForecastForTop()

weatherDataTESTER.getForecastForTop(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])


