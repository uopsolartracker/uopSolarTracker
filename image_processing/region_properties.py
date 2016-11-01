# !/usr/bin/python3
# Region Properties
import math
import numpy

def RegionProperties(Input,label):
    height, width = Input.shape # image assumed to be grayscale
    m00 = 0
    m01 = 0
    m10 = 0
    m11 = 0
    m20 = 0
    m02 = 0
    mu00 = 0
    mu01 = 0
    mu10 = 0
    mu11 = 0
    mu20 = 0
    mu02 = 0
    area = 0
    for x in range(0,height):
        for y in range(0,width):
            if(Input[x,y]==label):
                m00 = m00 + 1
                m01 = m01 + y
                m10 = m10 + x
                m11 = m11 + x*y
                m20 = m20 + x*x
                m02 = m02 + y*y
                area = area + 1
    xc = m10/m00
    yc = m01/m00
    for x in range(0,height):
        for y in range(0,width):
            if(Input[x,y]==label):
                mu01 = mu01 + (y - yc)
                mu10 = mu10 + (x - xc)
                mu11 = mu11 + (x - xc)*(y - yc)
                mu20 = mu20 + math.pow((x - xc),2)
                mu02 = mu02 + math.pow((y - yc),2)
    mu00 = m00

    return mu00, mu11, mu02, mu20, xc, yc

def PCA(mu00, mu11, mu02, mu20):
    eig_vals = [0,0]
    eig_vals[0] = 1/(2*mu00)*(mu20 + mu02 + math.sqrt(math.pow((mu20-mu02),2) + math.pow(4*mu11,2)))
    eig_vals[1] = 1/(2*mu00)*(mu20 + mu02 - math.sqrt(math.pow((mu20-mu02),2) + math.pow(4*mu11,2)))
    theta = 0.5*math.atan2(2*mu11,mu20-mu02)

    return eig_vals, theta

def GetAxes(xc, yc, theta, eig_vals):
    line1 = [[yc, yc],[xc, xc-25]]
    line2 = [[yc, yc-25],[xc, xc]]
    line3 = [[yc, yc+25],[xc, xc]]
    line4 = [[yc, yc],[xc, xc+25]]
    return line1, line2, line3, line4