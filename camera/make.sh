#!/bin/bash
clear

#arm-linux-gnueabihf-g++ capture.cpp -o startCapture -g -I -L -D_LIN -D_DEBUG -L./ -I./ -lpthread -I libusb/ -L libusb/ -DGLIBC_20 -march=armv7 -mcpu=cortex-m3 -mthumb -lASICamera2

#gcc capture.cpp -o startCapture -Wall -lASICamer2

arm-linux-gnueabihf-g++ capture.cpp -o startCapture `pkg-config --cflags --libs opencv` -l ASICamera2

