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

allCodes = len(idCodeList)

time = "2am"
if sys.argv[1] == 'n':	#night
	print("___Testing for night___")
	print("Input time: ", sys.argv[2])
	for a in range(allCodes):
		for b in range(allCodes):
			for c in range(allCodes):
				for d in range(allCodes):
					print("Inputs: Current_bad_weather: ", w, " ID_8am = ", idCodeList[a], " ID_11am: ", idCodeList[b], " ID_2pm: ", idCodeList[c], " ID_5pm: ", idCodeList[d])

#elif sys.argv[1] == 'd'	#day
p = weatherDataTESTER.getForecastForTop(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
print(p)


