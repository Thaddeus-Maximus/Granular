#!/usr/bin/env python

from __future__ import print_function
import Adafruit_BBIO.UART as UART
import serial

#UART.setup("UART1");

ser = serial.Serial(port = "/dev/ttyO1", baudrate=9600)
ser.close()
ser.open()
ch = ""
dist = 0;
while ser.isOpen():
	c = ser.read()
	if c == '\r':
		dist = float(ch)
		ch = ""
		print("Distance is %.1f cm" % dist)
		continue
	elif c in ['0','1','2','3','4','5','6','7','8','9']:
		ch += c

	print("%s" % c, end="")

UART.cleanup();
