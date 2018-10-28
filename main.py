#!/usr/bin/env python3

from __future__ import print_function
import Adafruit_BBIO.UART as UART
import serial
import time
import sys
#UART.setup("UART1");

ser = serial.Serial(port = "/dev/ttyO1", baudrate=9600, timeout=1.0)
ser.close()

ser.open()
ch = ""
dist = 0;
while ser.isOpen():
	try:
		ch = ser.read_until(b'\r')
#		print(ch)
		ch = ch.decode('utf-8', 'ignore')
		dist = float("".join(x for x in ch if x in ".1234567890"))
		print("Dist = %.1f cm" % dist)
		sys.stdout.flush()
	except ValueError:
		print("err: %s" % ch)
UART.cleanup();
