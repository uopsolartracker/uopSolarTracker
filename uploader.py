#!/usr/bin/python3

import subprocess
from base import base

### Description: Wrapper class to uplaod files to a preconfigured Dropbox account
###				 Used for taking the pictures from the RPi and making them easily accessible
class uploader(base):

	### Description: Wrapper function for uploading a file to the configred Dropbox account
	### Flow: 	1) Uplaods filename to Dropbox
	### Input: filename -> The full filename and extension of the file to be uploaded
	### Output: None
	### Example:
	### 	uploader.upload("sun_image.png")
	def upload(self, filename):
		self.LogM(20, "Uploading '" + filename + "' image to Dropbox")
		subprocess.call(["Dropbox-Uploader/dropbox_uploader.sh upload " + filename " /Images/", i])