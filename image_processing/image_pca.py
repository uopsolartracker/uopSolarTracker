# !/usr/bin/python3

import cv2
import numpy
from matplotlib import pyplot

if __name__ == '__main__':
	img = cv2.imread('Sun.JPG')
	
	# TODO: Add debug output if file does not load properly
	grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret,threshImg = cv2.threshold(grayImg, 127, 255, cv2.THRESH_BINARY)

	kernel = numpy.uint8([[0, 1, 0],[1, 1, 1],[0, 1, 0]])
	eroded = cv2.erode(threshImg, kernel, iterations = 2)
	dilated = cv2.erode(eroded, kernel, iterations = 2)


	
	pyplot.figure("Threshold Image")
	pyplot.imshow(threshImg, cmap = 'gray')
	pyplot.figure("Eroded Image")
	pyplot.imshow(eroded, cmap = 'gray')
	pyplot.figure("Dilated Image")
	pyplot.imshow(dilated, cmap = 'gray')

	pyplot.show()