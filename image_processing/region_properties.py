# !/usr/bin/python3
# Region Properties
import math

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
    for x in range(1:height)
            for y in range(1:width)
                if(Input(x,y)==label)
                    m00 = m00 + 1
                    m01 = m01 + y
                    m10 = m10 + x
                    m11 = m11 + x*y
                    m20 = m20 + x*x
                    m02 = m02 + y*y
                    area = area + 1
        xc = m10/m00
        yc = m01/m00
        for x in range(1:height)
            for y in range(1:width)
                if(Input(x,y)==label)
                    mu01 = mu10 + (y - yc)
                    mu10 = mu10 + (x - xc)
                    mu11 = mu11 + (x - xc)*(y - yc)
                    mu20 = mu20 + (x - xc)^2
                    mu02 = mu02 + (y - yc)^2
        mu00 = m00

    return mu00, mu11, mu02, mu20, xc, yc

def PCA(mu00, mu11, mu02, mu20):
	c = 1/mu00.*[[mu20, mu11],
                 [mu11, mu02]]
    eig_vals[1] = 1/(2*mu00)*(mu20 + mu02 + math.sqrt((mu20-mu02)^2 + 4*mu11^2))
    eig_vals[2] = 1/(2*mu00)*(mu20 + mu02 - math.sqrt((mu20-mu02)^2 + 4*mu11^2))
    theta = 0.5*math.atan2(2*mu11,mu20-mu02)

	return eig_vals, theta

def DrawAxes(xc, yc, theta, eigvals[]):
	line1 = [[yc, yc+math.sin(theta)*math.sqrt(eig_vals[1])],[xc, xc+math.cos(theta)*math.sqrt(eig_vals[1])]]
	line2 = [[yc, yc+math.sin(theta + math.pi/2)*math.sqrt(eig_vals[2])],[xc, xc+math.cos(theta + math.pi/2)*math.sqrt(eig_vals[2])]]
	line3 = [[yc, yc+math.sin(theta + math.pi)*math.sqrt(eig_vals[1])],[xc, xc+math.cos(theta + math.pi)*math.sqrt(eig_vals[1])]]
	line4 = [[yc, yc+math.sin(theta + 3*math.pi/2)*math.sqrt(eig_vals[2])],[xc, xc+math.cos(theta + 3*math.pi/2)*math.sqrt(eig_vals[2])]]
	return line1, line2, line3, line4