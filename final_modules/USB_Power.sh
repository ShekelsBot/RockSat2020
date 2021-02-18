#!/bin/bash
# Purpose of this is to mount and turn off power to USB ports so the camera can record
# Then transfer data once it has finished recording
# 
# Script uses Uhubctl
# Needs the drive to mount based on UUID
#
# https://github.com/mvp/uhubctl
# https://www.cyberciti.biz/faq/linux-mount-an-lvm-volume-partition-command/
#
DATE=$(date +%C%y%m%d)
#Get current date format in Century Year Month Day
#Corresponds to specific folder name
umount /mnt/usb-drive
cd uhubctl
uhubctl -a off -l 1-1
#Turn off power to the USB 2.0 Ports
sleep 3
echo "Turning on power to USB Ports"
uhubctl -a on -l 1-1
#Turn power back on the USB Ports
sleep 2
echo "Mounting Camera"
mount -a
echo "Camera is mounted under /media/usb-drive/"
cd /mnt/usb-drive/DCIM/$DATE
#Navigate to Specifc directory
#Use DATE value for specifc name of folder
echo "Copying AB.MP4 files"
find -iname '*AB.MP4' -exec cp {} /home/pi/data/ \;
#2 copies of files. AA is high quality. AB is lower quality.
echo "Finished"