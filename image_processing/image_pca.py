# !/usr/bin/python3

import cv2
import numpy
from matplotlib import pyplot
from region_properties import RegionProperties, PCA, GetAxes

if __name__ == '__main__':
	img = cv2.imread('Sun.JPG')
	
	# TODO: Add debug output if file does not load properly
	grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret,threshImg = cv2.threshold(grayImg, 127, 255, cv2.THRESH_BINARY)

	kernel = numpy.uint8([[0, 1, 0],[1, 1, 1],[0, 1, 0]])
	eroded = cv2.erode(threshImg, kernel, iterations = 2)
	dilated = cv2.erode(eroded, kernel, iterations = 2)

	mu00, mu11, mu02, mu20, xc, yc = RegionProperties(dilated, 0)
	eig_vals, theta = PCA(mu00, mu11, mu02, mu20)
	line1, line2, line3, line4 = GetAxes(xc, yc, theta, eig_vals)

	pyplot.figure("Threshold Image")
	pyplot.imshow(threshImg, cmap = 'gray')
	pyplot.figure("Eroded Image")
	pyplot.imshow(eroded, cmap = 'gray')
	pyplot.figure("Dilated Image")
	pyplot.imshow(dilated, cmap = 'gray')
	pyplot.figure("Original With Center (" + str(xc) + "," + str(yc) + ")")
	pyplot.imshow(grayImg, cmap = 'gray')
	pyplot.plot(line1[0],line1[1], 'k-')
	pyplot.plot(line2[0],line2[1], 'k-')
	pyplot.plot(line3[0],line3[1], 'k-')
	pyplot.plot(line4[0],line4[1], 'k-')

	pyplot.show()