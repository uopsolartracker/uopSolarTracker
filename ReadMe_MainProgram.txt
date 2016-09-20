This document outlines the intended flow our main program will take, and
how we should create libraries and objects of the lower level functions.

The flow of the program starts and ends with the scheduler, which controls
when the main program starts. Once the main program starts, we move through
various checks, on the weather, position of the sun, etc. All paths eventually
lead back to the scheduler, once bad weather is detected, or once the end of
the day has transpired

The primary functionality which should be encapsulated is as follows:
	1. Weather Information - The collecting, parsing, and all other
		logic about whether the weather is good to open the case
	2. Image Processing - The parsing and reporting of images to
		align the telescope
	3. Camera Control - The functionality to take, name, and store
		photos
	4. Motor Control - The functionality to direct the motors on the
		case and on the mirror
	5. Logging - The functionality to log events
	6. Any other fun ideas

A few other objects we should use, include:
	1. State of the enclosure - Information on whether it is open or closed
	2. State of the mirror - Information on the current position (relative to a
		predetermined point) and bounds checking for servo movement
	3. State of the camera - Information whether it exists and is working (images
		are not blank)

These more limited objects will essentially contain information about the
state of the physical components, and internally check for errors upon
initialization, runtime, and clean up.

The main program should use the above objects/libraries to run the entire
project. In addition, the main program will collate logs deemed important.