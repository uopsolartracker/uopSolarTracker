#!/usr/bin/python3

# Based of the PSA Algorithm for sun position
# Written by Jacquelin Rodriguez

import os               																				
import datetime	
import time
import math
import cmath
import sched

#constants that will not change throughout the calculation
pi = 3.14159265358979323846;
twopi = 2*pi;
rad = pi/180;
dEarthMeanRadius = 6371.01
dAstronmicalUnit = 149597890
dLongitude = -121.31190
dLatitude =37.97580



## --Calculating difference between current Julian Day and JD 2451545.0--
def ElapsedJD (Year, Month, Day, Hours, Minutes, Seconds):
	DecimalHours = float(Hours + (Minutes + (Seconds /60.0))/60.0)#Time of day in UTC decimal hours
	Aux1= (Month-14)/12;
	Aux2 = (1461*(Year +4800+Aux1))/4 +(367*(Month-2-(12*Aux1)))/12 - (3*((Year +4900+Aux1)/100))/4 + (Day-32075);
	JDate = float(Aux2) -0.5 + (DecimalHours)/24.0
	ElapJulianDays = JDate- 2451545.0 #Calculating difference between current Julian Day and JD
	
	return (ElapJulianDays, DecimalHours)

## -- Calulating ecliptic coordinates--
def EclipticCoordinates (ElapJulianDays):
	Omega = 2.1429 - 0.0010394594*ElapJulianDays;
	MeanLongitude = 4.8950630+ 0.017202791698*ElapJulianDays; # Radians
	MeanAnomaly = 6.2400600+ 0.0172019699*ElapJulianDays;
	EclipLongitude = MeanLongitude + 0.03341607* math.sin( MeanAnomaly ) + 0.00034894*math.sin( 2*MeanAnomaly )-0.0001134-0.0000203*math.sin(Omega);
	EclipObliquity = 0.4090928 - (6.2140e-9)*ElapJulianDays +0.0000396* math.cos(Omega);
	
	return (EclipLongitude, EclipObliquity)


## -- Calulating celestial coordinates--
def CelestialCoordinates(EclipLongitude, EclipObliquity, twopi):
	Sin_EclipLongitude= math.sin(EclipLongitude);
	Y=float(math.cos(EclipObliquity)*Sin_EclipLongitude);
	X=float(math.cos(EclipLongitude));
	RightAscension =math.atan2(Y,X);
	if RightAscension < 0.0 :
		RightAscension= RightAscension + twopi;

	Declination =math.asin(math.sin(EclipObliquity)*Sin_EclipLongitude);
	
	return (Declination, RightAscension)


## -- Calculating Local coordinates (azimuth and zenith angle)in degrees--
def LocalCoordinates (ElapJulianDays,DecimalHours,dLongitude, rad, RightAscension,Declination):
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
	
	return (ZenithAngle, Azimuth)

## -- Calculating Parallax Correction--
def ParallaxCorrection (dEarthMeanRadius, dAstronmicalUnit,ZenithAngle,rad):

	Parallax = (dEarthMeanRadius/dAstronmicalUnit)*math.sin(ZenithAngle);
	ZenithAngle=(ZenithAngle + Parallax)/rad;
	Elevation = 90-ZenithAngle;
	
	return (Elevation)



#-----MAIN CODE------	

#get timestamp and make it human readable
timeStamp= time.time();

humanReadable_TS= datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d-%H-%M-%S');
print (humanReadable_TS)

# parse human readable timestamp to create variables for year, month, day, etc.
h = humanReadable_TS.split("-");

Elevation_List= [];
Azimuth_List=[];
Hour_Lisit=[];

Year = float (h[0]);
Month = float(h[1]);
Day = float(h[2]);
Hour_List= [ 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]# list of times from 8am to 5pm in UTC 
	

for l in range(0,9):

	if Hour_List[l] >= 24.0:
		Day = Day + 1.0;	
		Hour_List[l] = Hour_List[l] - 24.0;
	if int(Month) == (1 | 3| 5 | 7 | 8 | 10) & int(Day) == 31:
		Month = Month +1;
		Day = 1;
	if int(Month) == (4 | 6 | 9 | 11) & int(Day) == 30:
		Month = Month +1;
		Day = 1;
	if int(Month) == 12 & int(Day) == 31:
		Month = 1;
		Year = Year +1;
		Day = 1;
	if int(Month) == 2 & 0 == (int(Year)%4) & int(Day) == 29:
		Month =Month +1;
		Day = 1;
	if int(Month) == 2 & 0 != (int(Year)%4) & int(Day)==28:
		Month = Month +1;
		Day = 1;
		
	Minutes = float(h[4]);
	Seconds = float(h[5]);
	
	JD_ElapsedJD = ElapsedJD (Year, Month, Day, Hour_List[l], Minutes, Seconds);
	
	EC_EclipticCoordinates = EclipticCoordinates (JD_ElapsedJD[0]);
	CC_CelestialCoordintes = CelestialCoordinates(EC_EclipticCoordinates[0], EC_EclipticCoordinates[1], twopi);
	LC_Azimuth = LocalCoordinates (JD_ElapsedJD[0],JD_ElapsedJD[1],dLongitude, rad, CC_CelestialCoordintes[1], CC_CelestialCoordintes[0])
	PC_Elevation = ParallaxCorrection (dEarthMeanRadius, dAstronmicalUnit,LC_Azimuth[0],rad);
	

	Elevation_List.insert (l,round(PC_Elevation,3));
	Azimuth_List.insert (l,round(LC_Azimuth[1],3));
	
print(Elevation_List, Azimuth_List)

	
	


		





