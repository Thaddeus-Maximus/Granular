#!/bin/bash

sudo apt update
sudo apt install python3
sudo apt install python3-pip

pip3 install pyserial
pip3 install blynk-library-python

(crontab -l ; echo "@reboot /root/granular/main.py")| crontab -
