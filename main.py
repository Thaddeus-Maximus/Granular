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

VPIN_ARM = 0
VPIN_DIST = 1
VPIN_THRESH = 2

dist = 0
armed = 1
thresh = 10
dist_hist = [25 for i in range(30)]

def move_average(new_dist):
	global dist_hist
#	print(dist_hist)
	dist_hist.append(new_dist)
	dist_hist.pop(0)
#	print(sum(dist_hist)/len(dist_hist))
	return sum(dist_hist)/len(dist_hist)

def serial_thread():
	global dist
	global blynk
	global armed
	global thresh
	ser = serial.Serial(port = "/dev/ttyO1", baudrate=9600, timeout=1.0)
	ser.close()

	ser.open()
	ch = ""
	armed = 1
	blynk.virtual_write(VPIN_ARM, armed)
	while ser.isOpen():
		try:
			ch = ser.read_until(b'\r')
#			print(ch)
			ch = ch.decode('utf-8', 'ignore')
			dist_raw = float("".join(x for x in ch if x in ".1234567890"))/30.48
			dist = move_average(dist_raw)
			blynk.virtual_write(VPIN_DIST, dist)
#			print("Dist = %.3f ft (filter = %.3f)" % (dist_raw, dist))
			sys.stdout.flush()
			if dist < thresh and armed:
				print('Sending alert...')
				armed = 0
				blynk.virtual_write(VPIN_ARM, 0)
				blynk.notify('YOUR GRAINBIN IS ABOUT TO OVERFLOW!')
		except ValueError:
			pass
#			print("err: %s" % ch)

#serial_thread()

t = threading.Thread(target=serial_thread)
t.start()

@blynk.VIRTUAL_WRITE(VPIN_ARM)
def arm_handler(val):
	global armed
	armed = int(val);
	print('Armed', armed)

@blynk.VIRTUAL_WRITE(VPIN_THRESH)
def thresh_handler(val):
	global thresh
	thresh = float(val);
	print('Thresh', thresh)

@blynk.VIRTUAL_READ(VPIN_DIST)
def my_read_handler():
	print('reading... %.3f' % dist)
	blynk.virtual_write(VPIN_DIST, dist)

blynk.run()
