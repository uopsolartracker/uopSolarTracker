import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('some_picture.jph',0)
edges = cv2.Canny(img,100,200,3,1)

