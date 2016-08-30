This document outlines the intended flow our main program will take, and
how we should create libraries and objects of the lower level functions.

The primary functionality which should be encapsulated is as follows:
	1. Weather Information - The collecting, parsing, and all other
		logic about whether the weather is good to open the case
	2. Image Processing - The parsing and reporting of images to
		align the telescope
	3. Camera Control - The functionality to take, name, and store
		photos
	4. Motor Control - The functionality to direct the motors on the
		case and on the mirror
	5. Logging - The functionality to log events (this might not be
		necessary, but could be handy to have one method of logging
		which all other objects/libraries use)
	6. Any other fun ideas

The main program should use the above objects/libraries to run the entire
project. In addition, the main program will collate logs deemed important.