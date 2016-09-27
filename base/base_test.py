#!/usr/bin/python3

# Test script for the base class and logging
import base

class test(base.base): # Inheriting from the base class, from the base module (so base-ic...)
	def do_stuff(self):
		print ("Hey, I can print to the console too!")
		self.LogM(10, "Successfully printed to the console") # Type of debug message

class othertest(base.base):
	def do_otherstuff(self):
		print ("Printing to the console is a synch")
		self.LogM(10, "Successfully printed to the console") # Type of debug message

if __name__ == '__main__':
	mytest = test("test")
	myothertest = othertest("other_test")
	mytest.LogM(10, "This is a debug mesasage")
	mytest.LogM(20, "This is an info mesasage")
	mytest.LogM(30, "This is a warning mesasage")
	mytest.LogM(40, "This is an error mesasage")
	mytest.LogM(50, "This is a critical mesasage")
	myothertest.LogM(30, "We out...")

	mytest.do_stuff()
	myothertest.do_otherstuff()

	print (mytest.Log_inst)
	print (myothertest.Log_inst)
