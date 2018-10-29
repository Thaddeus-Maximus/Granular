#!/usr/bin/env python3

import BlynkLib
import time

BLYNK_AUTH = '922fe4c0f7be485b912bd5bb9dfc00d8'

blynk = BlynkLib.Blynk(BLYNK_AUTH)

@blynk.VIRTUAL_READ(2)
def my_read_handler():
	print('reading...')
	blynk.virtual_write(2, 50);

blynk.run()
