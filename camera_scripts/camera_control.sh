#!/bin/bash
# Purpose of this is to mount and turn off power to USB ports so the camera can record
# Then transfer data once it has finished recording
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
python record.py
sleep 10
cd /home/pi/uhubctl
echo "Turning on power to USB Ports"
uhubctl -a on -l 1-1
#Turn power back on the USB Ports
sleep 3
echo "Mounting Camera"
sleep 5
mount -a
sleep 1
echo "Camera is mounted under /media/usb-drive/"
cd /mnt/usb-drive/DCIM/$DATE
#Navigate to Specifc directory
#Use DATE value for specifc name of folder
echo "Copying AB.MP4 files"
find -iname '*AB.MP4' -exec cp {} /home/pi/data/ \;
#2 copies of files. AA is high quality. AB is lower quality.
echo "Files copied"
cd /home/pi/camera_scripts
python power_off.py
echo "Shutting down"
