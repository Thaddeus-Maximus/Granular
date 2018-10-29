#!/usr/bin/env python3

from __future__ import print_function
import Adafruit_BBIO.UART as UART
import serial
import time
import sys
import BlynkLib
import time
import threading

BLYNK_AUTH = '922fe4c0f7be485b912bd5bb9dfc00d8'
blynk = BlynkLib.Blynk(BLYNK_AUTH)
#UART.setup("UART1");

dist = 0

def serial_thread():
	global dist
	global blynk
	ser = serial.Serial(port = "/dev/ttyO1", baudrate=9600, timeout=1.0)
	ser.close()

	ser.open()
	ch = ""
	while ser.isOpen():
		try:
			ch = ser.read_until(b'\r')
#			print(ch)
			ch = ch.decode('utf-8', 'ignore')
			dist = float("".join(x for x in ch if x in ".1234567890"))/30.48
#			print("Dist = %.1f cm" % dist)
			sys.stdout.flush()
			if dist < 3:
				blynk.notify('YOUR GRAINBIN IS ABOUT TO OVERFLOW!')
		except ValueError:
			pass
#			print("err: %s" % ch)

t = threading.Thread(target=serial_thread)
t.start()

@blynk.VIRTUAL_READ(2)
def my_read_handler():
	print('reading... %.3f' % dist)
	blynk.virtual_write(2, dist)

blynk.run()
