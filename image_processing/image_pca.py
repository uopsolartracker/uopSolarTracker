# !/usr/bin/python3

import cv2
import numpy
from matplotlib import pyplot

if __name__ == '__main__':
	img = cv2.imread('Sun.JPG')
	if (!img.data || img.empty()):
		# TODO: Add debug output if file does not load properly
		exit(-1)

	cv2.cvtColor(img,grayImg, CV_BGR2GRAY)
	cv2.threshold(grayImg, threshImg, 50, 255, CV_THRESH_BINARY | CV_THRESH_OTSU)

	pyplot.imshow(threshImg, cmap = 'gray')