#!/usr/bin/python3

# Region Properties
import cv2
import math
import numpy

def RegionProperties(Input,label):
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

    return xc, yc

def GetCenter(img):
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,threshImg = cv2.threshold(grayImg, 60, 255, cv2.THRESH_BINARY)
    # cv2.imwrite('sun_thresh.bmp',threshImg)
    # TODO: Turn imwrite into a debug output to be stored for later debugging

    mu00, mu11, mu02, mu20, xc, yc = RegionProperties(threshImg,255)
    return xc, yc

# The purpose of GetAxes() is for debugging, to visually show where the axes are drawn
def GetAxes(xc, yc):
    line1 = [[yc, yc],[xc, xc-25]]
    line2 = [[yc, yc-25],[xc, xc]]
    line3 = [[yc, yc+25],[xc, xc]]
    line4 = [[yc, yc],[xc, xc+25]]
    return line1, line2, line3, line4