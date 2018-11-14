#!/bin/bash

stty -F /dev/ttyO1 cs8 -parenb -cstopb
/root/project/main.py
