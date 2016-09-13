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


#p = weatherDataTESTER.getForecastForTop(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
#p = json.dumps(p, sort_keys=True, indent=4)
#print(p)

allCodes = len(idCodeList)

time = ['2am', '8am', '11am', '2pm', '5pm']
w = [0, 1]	# 1 = currently bad weather, 0 = currently good weather

sys.stdout = open("forecast_good_current_weather_2am_test.txt", "w")	
print("___Test in good weather___")
print("Input time: ", time[0])
print("_______________________________________________________________________________")
for a in range(allCodes):
	for b in range(allCodes):
		for c in range(allCodes):
			for d in range(allCodes):
				print("Inputs: Current_bad_weather: ", w[0], " ID_8am = ", idCodeList[a], " ID_11am: ", idCodeList[b], " ID_2pm: ", idCodeList[c], " ID_5pm: ", idCodeList[d], "Time: ", time[0])
				print(json.dumps(weatherDataTESTER.getForecastForTop(w[0], idCodeList[a],  idCodeList[b],  idCodeList[c],  idCodeList[d], time[0]), sort_keys=True, indent = 4))
				print("")
sys.stdout.close()

sys.stdout = open("forecast_good_current_weather_8am_test.txt", "w")	
print("___Test in good weather___")
print("Input time: ", time[1])
print("_______________________________________________________________________________")
for a in range(allCodes):
	for b in range(allCodes):
		for c in range(allCodes):
			for d in range(allCodes):
				print("Inputs: Current_bad_weather: ", w[0], " ID_8am = ", idCodeList[a], " ID_11am: ", idCodeList[b], " ID_2pm: ", idCodeList[c], " ID_5pm: ", idCodeList[d], "Time: ", time[1])
				print(json.dumps(weatherDataTESTER.getForecastForTop(w[0], idCodeList[a],  idCodeList[b],  idCodeList[c],  idCodeList[d], time[1]), sort_keys=True, indent = 4))
				print("")
sys.stdout.close()

sys.stdout = open("forecast_good_current_weather_11am_test.txt", "w")	
print("___Test in good weather___")
print("Input time: ", time[2])
print("_______________________________________________________________________________")
for a in range(allCodes):
	for b in range(allCodes):
		for c in range(allCodes):
			for d in range(allCodes):
				print("Inputs: Current_bad_weather: ", w[0], " ID_8am = ", idCodeList[a], " ID_11am: ", idCodeList[b], " ID_2pm: ", idCodeList[c], " ID_5pm: ", idCodeList[d], "Time: ", time[2])
				print(json.dumps(weatherDataTESTER.getForecastForTop(w[0], idCodeList[a],  idCodeList[b],  idCodeList[c],  idCodeList[d], time[2]), sort_keys=True, indent = 4))
				print("")
sys.stdout.close()

sys.stdout = open("forecast_good_current_weather_2pm_test.txt", "w")	
print("___Test in good weather___")
print("Input time: ", time[3])
print("_______________________________________________________________________________")
for a in range(allCodes):
	for b in range(allCodes):
		for c in range(allCodes):
			for d in range(allCodes):
				print("Inputs: Current_bad_weather: ", w[0], " ID_8am = ", idCodeList[a], " ID_11am: ", idCodeList[b], " ID_2pm: ", idCodeList[c], " ID_5pm: ", idCodeList[d], "Time: ", time[3])
				print(json.dumps(weatherDataTESTER.getForecastForTop(w[0], idCodeList[a],  idCodeList[b],  idCodeList[c],  idCodeList[d], time[3]), sort_keys=True, indent = 4))
				print("")
sys.stdout.close()

sys.stdout = open("forecast_good_current_weather_5pm_test.txt", "w")	
print("___Test in good weather___")
print("Input time: ", time[4])
print("_______________________________________________________________________________")
for a in range(allCodes):
	for b in range(allCodes):
		for c in range(allCodes):
			for d in range(allCodes):
				print("Inputs: Current_bad_weather: ", w[0], " ID_8am = ", idCodeList[a], " ID_11am: ", idCodeList[b], " ID_2pm: ", idCodeList[c], " ID_5pm: ", idCodeList[d], "Time: ", time[4])
				print(json.dumps(weatherDataTESTER.getForecastForTop(w[0], idCodeList[a],  idCodeList[b],  idCodeList[c],  idCodeList[d], time[4]), sort_keys=True, indent = 4))
				print("")
sys.stdout.close()

sys.stdout = open("forecast_bad_current_weather_2am_test.txt", "w")
print("___Test in bad weather___")
print("Input time: ", time[0])
print("_______________________________________________________________________________")
for a in range(allCodes):
	for b in range(allCodes):
		for c in range(allCodes):
			for d in range(allCodes):
				print("Inputs: Current_bad_weather: ", w[1], " ID_8am = ", idCodeList[a], " ID_11am: ", idCodeList[b], " ID_2pm: ", idCodeList[c], " ID_5pm: ", idCodeList[d], "Time: ", time[0])
				print(json.dumps(weatherDataTESTER.getForecastForTop(w[1], idCodeList[a],  idCodeList[b],  idCodeList[c],  idCodeList[d], time[0]), sort_keys=True, indent = 4))
				print("")
sys.stdout.close()

sys.stdout = open("forecast_bad_current_weather_8am_test.txt", "w")
print("___Test in bad weather___")
print("Input time: ", time[1])
print("_______________________________________________________________________________")
for a in range(allCodes):
	for b in range(allCodes):
		for c in range(allCodes):
			for d in range(allCodes):
				print("Inputs: Current_bad_weather: ", w[1], " ID_8am = ", idCodeList[a], " ID_11am: ", idCodeList[b], " ID_2pm: ", idCodeList[c], " ID_5pm: ", idCodeList[d], "Time: ", time[1])
				print(json.dumps(weatherDataTESTER.getForecastForTop(w[1], idCodeList[a],  idCodeList[b],  idCodeList[c],  idCodeList[d], time[1]), sort_keys=True, indent = 4))
				print("")
sys.stdout.close()

sys.stdout = open("forecast_bad_current_weather_11am_test.txt", "w")
print("___Test in bad weather___")
print("Input time: ", time[2])
print("_______________________________________________________________________________")
for a in range(allCodes):
	for b in range(allCodes):
		for c in range(allCodes):
			for d in range(allCodes):
				print("Inputs: Current_bad_weather: ", w[1], " ID_8am = ", idCodeList[a], " ID_11am: ", idCodeList[b], " ID_2pm: ", idCodeList[c], " ID_5pm: ", idCodeList[d], "Time: ", time[2])
				print(json.dumps(weatherDataTESTER.getForecastForTop(w[1], idCodeList[a],  idCodeList[b],  idCodeList[c],  idCodeList[d], time[2]), sort_keys=True, indent = 4))
				print("")
sys.stdout.close()

sys.stdout = open("forecast_bad_current_weather_2pm_test.txt", "w")
print("___Test in bad weather___")
print("Input time: ", time[3])
print("_______________________________________________________________________________")
for a in range(allCodes):
	for b in range(allCodes):
		for c in range(allCodes):
			for d in range(allCodes):
				print("Inputs: Current_bad_weather: ", w[1], " ID_8am = ", idCodeList[a], " ID_11am: ", idCodeList[b], " ID_2pm: ", idCodeList[c], " ID_5pm: ", idCodeList[d], "Time: ", time[3])
				print(json.dumps(weatherDataTESTER.getForecastForTop(w[1], idCodeList[a],  idCodeList[b],  idCodeList[c],  idCodeList[d], time[3]), sort_keys=True, indent = 4))
				print("")
sys.stdout.close()

sys.stdout = open("forecast_bad_current_weather_5pm_test.txt", "w")
print("___Test in bad weather___")
print("Input time: ", time[4])
print("_______________________________________________________________________________")
for a in range(allCodes):
	for b in range(allCodes):
		for c in range(allCodes):
			for d in range(allCodes):
				print("Inputs: Current_bad_weather: ", w[1], " ID_8am = ", idCodeList[a], " ID_11am: ", idCodeList[b], " ID_2pm: ", idCodeList[c], " ID_5pm: ", idCodeList[d], "Time: ", time[4])
				print(json.dumps(weatherDataTESTER.getForecastForTop(w[1], idCodeList[a],  idCodeList[b],  idCodeList[c],  idCodeList[d], time[4]), sort_keys=True, indent = 4))
				print("")
sys.stdout.close()


