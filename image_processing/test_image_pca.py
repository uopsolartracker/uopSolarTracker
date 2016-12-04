# !/usr/bin/python3

import cv2
import numpy
from matplotlib import pyplot
from region_properties import region_properties

if __name__ == '__main__':
	img = cv2.imread('sun_gray.bmp')

	rp = region_properties
	
	# TODO: Add debug output if file does not load properly
	grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret,threshImg = cv2.threshold(grayImg, 60, 255, cv2.THRESH_BINARY)
	# cv2.imwrite('sun_thresh.bmp',threshImg)
	# TODO: Turn imwrite into a debug output to be stored for later debugging

	xc, yc = rp.RegionProperties(threshImg,255)
	line1, line2, line3, line4 = rp.GetAxes(xc, yc)

	pyplot.figure("Threshold Image")
	pyplot.imshow(threshImg, cmap = 'gray')
	pyplot.figure("Original With Center (" + str(xc) + "," + str(yc) + ")")
	pyplot.imshow(grayImg, cmap = 'gray')
	pyplot.plot(line1[0],line1[1], 'k-')
	pyplot.plot(line2[0],line2[1], 'k-')
	pyplot.plot(line3[0],line3[1], 'k-')
	pyplot.plot(line4[0],line4[1], 'k-')

	pyplot.show()
