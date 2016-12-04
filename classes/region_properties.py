#!/usr/bin/python3

# Region Properties
import cv2
import math
import numpy
from base import base

### Description: The region_properties class will be used to find the "center" of the sun, returning the pixel location
### This class contains the function GetCenter, which takes an image of the sun, and returns its "center" based on pixel location
class region_properties(base):
    ### Description: This function perfroms "Principle Component Analysis" on the image passed to GetCenter()
    ###
    ### Flow: --> Image and pixel intensity (label) are arguments
    ###     --> Perform Principle Component Analysis on the image, using the label as the pixels to operate on
    ### Input: Image, pixel intensity
    ### Output: Pixel location of the "center" (height, width)
    def RegionProperties(Input,label):
        self.LogM(20, "Starting the region properties analysis to find the coordinates for the center of the sun")
        height, width = Input.shape # image assumed to be grayscale
        m00 = 0
        m01 = 0
        m10 = 0
        for x in range(0,height):
            for y in range(0,width):
                if(Input[x,y]==label):
                    m00 = m00 + 1
                    m01 = m01 + y
                    m10 = m10 + x
        xc = m10/m00
        yc = m01/m00

        self.LogM(10, "Found coordinates are ({x}, {y})".format(x=xc, y=yc))
        return xc, yc

    ### Description: Finds the "center" of an image of the sun
    ###
    ### Flow: --> Convert input image to grayscale
    ###     --> Threshold the image
    ###     --> Perform "Principle Component Analysis" on the thresholded image
    ### Inputs: Image of the sun
    ### Outputs: Pixel location of the "center" of the sun in the image, the height and width of the input image
    def GetCenter(img):
        self.LogM(20, "Starting to process image to find the center of the sun")
        grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Unnecessary for images which are already grayscale
        ret,threshImg = cv2.threshold(grayImg, 60, 255, cv2.THRESH_BINARY)

        # The imwrite is stored for debugging
        timeString = datetime.datetime.now()
        cv2.imwrite('processed_images\sun_thresh' + timeString + '.bmp',threshImg)

        mu00, mu11, mu02, mu20, xc, yc = RegionProperties(threshImg,255)
        height, width = Input.shape
        self.LogM(20, "Returning the center as ({x} ,{y}) and the height and width as {h}x{w}".format(x=xc,y=yc,h=height,w=width))
        return xc, yc, height, width

    # The purpose of GetAxes() is for debugging, to visually show where the axes are drawn
    #
    # Not used in the main program
    def GetAxes(xc, yc):
        line1 = [[yc, yc],[xc, xc-25]]
        line2 = [[yc, yc-25],[xc, xc]]
        line3 = [[yc, yc+25],[xc, xc]]
        line4 = [[yc, yc],[xc, xc+25]]
        return line1, line2, line3, line4