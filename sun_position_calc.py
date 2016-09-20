#!/usr/bin/python3

# Based of the PSA Algorithm for sun position
# Written by Jacquelin Rodriguez

import os               											
import xml									
import datetime	
import time
import math
import cmath

#constants that will not change throughout the calculation
pi = 3.14159265358979323846;
twopi = 2*pi;
rad = pi/180;
dEarthMeanRadius = 6371.01
dAstronmicalUnit = 149597890
dLongitude = -121.31190
dLatitude =37.97580

#get timestamp and make it human readable
timeStamp= time.time()
print (timeStamp)

humanReadable_TS= datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d-%H-%M-%S');
print (humanReadable_TS)

# parse human readable timestamp to create variables for year, month, day, etc.
h = humanReadable_TS.split("-")
print(h)

Year = float(h[0]);
Month = float(h[1]);
Day = float(h[2]);
Hours = float(h[3])+7.0; # Added 7hr to have tim ben UTC
Minutes = float(h[4]);
Seconds = float(h[5]);

## --Calculating difference between current Julian Day and JD 2451545.0--

#Time of day in UT decimal hours
DecimalHours = float(Hours + (Minutes + (Seconds /60.0))/60.0)

#Calculating current Julian Day
liAux1= (Month-14)/12;
liAux2 = (1461*(Year +4800+liAux1))/4 +(367*(Month-2-(12*liAux1)))/12 - (3*((Year +4900+liAux1)/100))/4 + (Day-32075);
JDate = float(liAux2) -0.5 + (DecimalHours)/24.0

#Calculating difference between current Julian Day and JD
ElapJulianDays = JDate- 2451545.0
print(ElapJulianDays)

## -- Calulating ecliptic coordinates--

Omega = 2.1429 - 0.0010394594*ElapJulianDays;
MeanLongitude = 4.8950630+ 0.017202791698*ElapJulianDays; # Radians
MeanAnomaly = 6.2400600+ 0.0172019699*ElapJulianDays;
EclipLongitude = MeanLongitude + 0.03341607* math.sin( MeanAnomaly ) + 0.00034894*math.sin( 2*MeanAnomaly )-0.0001134-0.0000203*math.sin(Omega);
EclipObliquity = 0.4090928 - (6.2140e-9)*ElapJulianDays +0.0000396* math.cos(Omega);


## -- Calulating celestial coordinates--

Sin_EclipLongitude= math.sin(EclipLongitude);
Y=float(math.cos(EclipObliquity)*Sin_EclipLongitude);
X=float(math.cos(EclipLongitude));
RightAscension =math.atan2(Y,X);
if RightAscension < 0.0 :
	RightAscension= RightAscension + twopi;

Declination =math.asin(math.sin(EclipObliquity)*Sin_EclipLongitude)


## -- Local coordinates (azimuth and zenith angle)in degrees--

GreenwichMeanSiderealTime = 6.6974243242 + 0.0657098283*ElapJulianDays + DecimalHours;
LocalMeanSiderealTime = (GreenwichMeanSiderealTime*15 + dLongitude)*rad;
HourAngle = LocalMeanSiderealTime-RightAscension;

Latidude_rad =dLatitude*rad;
Cos_Latitude = math.cos(Latidude_rad);
Sin_latitude = math.sin(Latidude_rad);
Cos_HourAngle = math.cos(HourAngle);

ZenithAngle = (math.acos(Cos_Latitude*Cos_HourAngle*math.cos(Declination)+math.sin(Declination)*Sin_latitude));
Y= float(-math.sin(HourAngle));
X= float(math.tan(Declination)*Cos_Latitude-Sin_latitude*math.cos(HourAngle));
Azimuth = math.atan2(Y,X);
if Azimuth < 0.0:
	Azimuth = Azimuth +twopi;

Azimuth = Azimuth/rad;

#Parallax Correction
Parallax= (dEarthMeanRadius/dAstronmicalUnit)*math.sin(ZenithAngle);
ZenithAngle=(ZenithAngle + Parallax)/rad;
Elevation = 90-ZenithAngle;
print(Azimuth, Elevation)
