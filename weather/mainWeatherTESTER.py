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

if str(sys.argv[1]) == 'n':	# Night Testing
	sys.stdout = open("weather_night_test.txt", "w")	
	print("Test file for getWeatherForTop() during the night")
	timeString = datetime.datetime.now()
	print("Current time of test: ", timeString)
	print("")

	for i in range(len(idCodeList)):
		print("Night testing.........................")
		timeStrNight = str(datetime.date.today()) + ' 05:00:0'
		timeStampNight = datetime.datetime.strptime(timeStrNight, "%Y-%m-%d %H:%M:%S").timestamp()	# float type
		idcode_test = idCodeList[i]
		timeStamp_test = timeStampNight
		weatherDataTESTER.getWeatherForTop(idcode_test, timeStamp_test)
		print("TopCoverCodes = ", json.dumps(weatherDataTESTER.topCoverCodes, sort_keys=True, indent=4))
		print("")

	sys.stdout.close()
elif str(sys.argv[1]) == 'd':	# Day Testing
	sys.stdout = open("weather_day_test.txt", "w")
	print("Test file for getWeatherForTop() during the day")
	timeString = datetime.datetime.now()
	print("Current time of test: ", timeString)

	for i in range(len(idCodeList)):
		print("Day testing.........................")
		timeStrDay = str(datetime.date.today()) + ' 08:10:0'
		timeStampDay = datetime.datetime.strptime(timeStrDay, "%Y-%m-%d %H:%M:%S").timestamp()	# float type
		weatherDataTESTER.getWeatherForTop(idCodeList[i], timeStampDay)
		print("TopCoverCodes = ", json.dumps(weatherDataTESTER.topCoverCodes, sort_keys=True, indent=4))
		for j in range(52):				### 8:00am, 8:10am, 8:20am, ... , 4:50pm, 5:00pm	
			timeStampDay = timeStampDay + TENMIN
			weatherDataTESTER.getWeatherForTop(idCodeList[i], timeStampDay)
			print("TopCoverCodes = ", json.dumps(weatherDataTESTER.topCoverCodes, sort_keys=True, indent=4))
			print("")

	sys.stdout.close()

