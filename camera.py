#!/usr/bin/python3

import subprocess
import os
from time import strftime, localtime
from base import base

### Description: Class contains the relevant info on the camera as well as controlling it to take pictures
class camera(base):

	### Description: Wrapper function for uploading a file to the configred Dropbox account
	### Flow: 	1) Calls binary to capture image
	###			2) Moves image from the camera/ folder to the images/ folder for further use
	### Input: fNone
	### Output: None
	### Example:
	### 	uploader.upload("sun_image.png")
	def capture_image(self):
		filename = strftime("%Y-%m-%d__%H_%S", localtime()) + ".png"
		self.LogM(20, "Going to capture an image named '" + filename + "' with the camera")
		subprocess.call(["camera/startCapture", filename])
		self.LogM(10, "Going to move '" + filename + "' to images/ folder")
		os.rename("camera/" + filename, "images/" + filename)
		self.LogM(10, "Moved '" + filename + "' to images/ folder")

	# In future versions, use this to get the status of the camera, and store it in instanced variables
	def get_status(self):
		pass
