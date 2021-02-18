#!/bin/bash
# Purpose of this is to mount and turn off power to USB ports so the camera can record
# Then transfer data once it has finished recording
#!/bin/bash
# 
# Script uses Uhubctl
# Needs the drive to mount based on UUID
#
# https://github.com/mvp/uhubctl
# https://www.techrepublic.com/article/how-to-properly-automount-a-drive-in-ubuntu-linux/
#
DATE=$(date +%C%y%m%d)
#Get current date format in Century Year Month Day
#Corresponds to specific folder name
#
cd /home/pi/uhubctl
uhubctl -a off -l 1-1
#Turn off power to the USB 2.0 Ports
sleep 3
cd /home/pi/camera_scripts
python power_on.py
sleep 3
python record_on.py