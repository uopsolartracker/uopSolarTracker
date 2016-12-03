#!/usr/bin/python3

# Based of the PSA Algorithm for sun position
# Written by Jacquelin Rodriguez

# python libraries 
import os               																				
import datetime	
import time
import math
import cmath
import sched  
import xlsxwriter 

pi = 3.14159265358979323846;
twopi = 2*pi;
rad = pi/180;
dEarthMeanRadius = 6371.01
dAstronmicalUnit = 149597890 #Earth center To Sun center in km
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
	
	return (Elevation, ZenithAngle)
	
## ---truncate function---
def truncate (f, n):
 	#Truncate a float f to n decimal places without rounding'''
 	s = '%.12f' % f
 	i, p, d = s.partition('.')
 	return ('.'.join([i, (d+'0'*n)[:n]]));
	
### ----------MAIN CODE-------------
def _hourly_position_():
	# get timestamp 
	timeStamp= time.time();

	# convert timestamp to humanreadable form
	humanReadable_TS= datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d-%H-%M-%S');

	# parse human readable to create variables for year, month, day, etc.
	h = humanReadable_TS.split("-");

	Hour_Lisit=[];
	List =[];

	Year = float (h[0]); # from humanreadable Year
	Month = float(h[1]); # from humanreadable Month
	Day = float(h[2]); # from humanreadable Day
	#Hour = [8 , 9, 10, 11, 12, 13, 14, 15, 16, 17 ];

	#Hour_List= [ 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]# list of times from 8am to 5pm in UTC 
	Hour= float(h[3]);
	Minutes = float(h[4]); # minutes set to 30
	Seconds = float(30); # seconds set to 30
	
	### constants that will not change throughout the script
	pi = 3.14159265358979323846;
	twopi = 2*pi;
	rad = pi/180;
	dEarthMeanRadius = 6371.01
	dAstronmicalUnit = 149597890 #Earth center To Sun center in km
	dLongitude = -121.31190
	dLatitude =37.97580
	
	# creates empty lists for Elevation, Azimuth, and Zenith angles
	Elevation_List= [];
	Azimuth_List= [];
	Zenith_List= [];
	x_azimuth=[];
	y_zenith=[];
	motor_azimuth=[];
	motor_zenith=[];	

	#for l in range(0,9):


	#--- if statements check to see if hr > 24 in UTC and changes day, month, or 
	#    year depending on the situation

	# checks to see if month is Jan, Mar, May, Jul, Aug,or Oct and day is 31st 
	if int(Month) == (1 | 3| 5 | 7 | 8 | 10) & int(Day) == 31 & Hour_List[l] == 24.0: 
		Month = Month +1; # increase month
		Day = 1; # day 31st -> 1st
	
	# checks to see if month is Jan, Mar, May, Jul, Aug,or Oct and day is not 31st
	if  int(Month) == (1 | 3| 5 | 7 | 8 | 10) & int(Day) != 31 & Hour_List[l] == 24.0: 
		Day = Day + 1; # day increased
	
	# checks to see if month is  Apr, Jun, Sep, or Nov and day is 30th 
	if int(Month) == (4 | 6 | 9 | 11) & int(Day) == 30 & Hour_List[l] == 24.0:
		Month = Month +1; # increase month
		Day = 1; # day 30th -> 1st
	
	# checks to see if month is  Apr, Jun, Sep, or Nov and day is not 30th 
	if int(Month) == (4 | 6 | 9 | 11) & int(Day) != 30 & Hour_List[l] == 24.0: 
		Day = Day + 1; # day increased
		
	# checks to see if month is Dec and day s 31st
	if int(Month) == 12 & int(Day) == 31 & Hour_List[l] == 24.0:
		Month = 1; # change month to Jan
		Year = Year +1; # increase year
		Day = 1; # day 31st -> 1st
		
	# checks to see month is Dec and day is not 31st	
	if int(Month) == 12 & int(Day) != 31 :
		Day = Day +1; # increase day
		
	# checks to see if month is Feb and if it's a leap year
	if int(Month) == 2 & 0 == (int(Year)%4) & int(Day) == 29 & Hour_List[l] == 24.0:
		Month = Month +1; # increase year
		Day = 1; # day 29th -> 1st
		
	# checks to see if month is Feb and not day is not 29th	
	if int(Month) == 2 & 0 == (int(Year)%4) & int(Day) != 29:
		Day = Day +1; # increase year
		
	# checks to see if month is Feb and if not a leap year
	if int(Month) == 2 & 0 != (int(Year)%4) & int(Day)==28 & Hour_List[l] == 24.0:
		Month = Month +1; # increase year
		Day = 1; # day 28th -> 1st
	
	# checks to see if month is Feb an day is not 28th
	if int(Month) == 2 & 0 != (int(Year)%4) & int(Day)!=28:
		Day = Day +1; # increase year
		
	
	# Calls functions that compute Azimuth and Elevation Angles
	JD_ElapsedJD = ElapsedJD (Year, Month, Day, Hour, Minutes, Seconds);
	EC_EclipticCoordinates = EclipticCoordinates (JD_ElapsedJD[0]);
	CC_CelestialCoordintes = CelestialCoordinates(EC_EclipticCoordinates[0], EC_EclipticCoordinates[1], twopi);
	LC_Azimuth = LocalCoordinates (JD_ElapsedJD[0],JD_ElapsedJD[1],dLongitude, rad, CC_CelestialCoordintes[1], CC_CelestialCoordintes[0])
	PC_Elevation = ParallaxCorrection (dEarthMeanRadius, dAstronmicalUnit,LC_Azimuth[0],rad);
	
	# Inserts Elevation and Azimuth Angles into corresponding lists
	#Elevation_List.insert (l,PC_Elevation[0]);
	Zenith_List.insert (0,PC_Elevation[1]);
	Azimuth_List.insert (0,LC_Azimuth[1]);
	
	#---Converting sun position angle to servo angle range motor command for azimuth and zenith--
	
	x_azimuth.insert(0,0.325*round(Azimuth_List[0]/0.325))
	y_zenith.insert (0,0.325*round((Zenith_List[0]+150)/0.325))
	
	x_azimuth[0]=truncate(x_azimuth[0], 4)
	y_zenith[0]=truncate(y_zenith[0], 4)
	
	motor_azimuth.insert(0,int(float(x_azimuth[0])/0.325));
	motor_zenith.insert(0,int(float(y_zenith[0])/0.325));
		
	excel_position(Azimuth_List,Zenith_List,Month,Day, Year);
		
	return (motor_azimuth,motor_zenith)
						
	
##----export sun position date to excel----
def excel_position(x_azimuth,y_zenith,Month,Day, Year):
	# Create an new Excel file and add a worksheet.
	workbook = xlsxwriter.Workbook('sun_postion_data'+'_'+str(int(Month))+'_'+str(int(Day))+'_'+str(int(Year))+ '.xlsx')
	worksheet = workbook.add_worksheet()

	# Widen the second and third column to make the text clearer.
	worksheet.set_column('B:B', 20)
	worksheet.set_column('C:C', 20)
	worksheet.set_column('D:D', 20)

	# Writing to first row and making text bold
	bold = workbook.add_format({'bold': True})
	worksheet.write('A1', 'Time', bold)
	worksheet.write('B1', 'Zenith Angle', bold)
	worksheet.write('C1', 'Azimuth Angle', bold)

	# Dictionary that has sun position data based on time of day
	data = (
		 ['8:30',  y_zenith[0], x_azimuth[0]],
		 #['9:30',  y_zenith[1], x_azimuth[1]],
		 #['10:30', y_zenith[2], x_azimuth[2]],
		 #['11:30', y_zenith[3], x_azimuth[3]],
		 #['12:30', y_zenith[4], x_azimuth[4]],
		 #['13:30', y_zenith[5], x_azimuth[5]],
		 #['14:30', y_zenith[6], x_azimuth[6]],
		 #['15:30', y_zenith[7], x_azimuth[7]],
		 #['16:30', y_zenith[8], x_azimuth[8]],
		 )

	row = 1;
	col = 0;

	# iterates over the data and writes it out row by row.
	for time,Zen,Azi in (data):
		worksheet.write(row, col, time)
		worksheet.write(row, col + 1, Zen)
		worksheet.write(row, col + 2, Azi)
		#row += 1
		
	# closes excel sheet
	workbook.close()	

	
_hourly_position_()	
	
	
	

	
	


	
	


		





