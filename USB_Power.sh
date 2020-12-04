#!/bin/bash
DATE=$(date +%C%y%m%d)
#Get current date format in Century Year Month Day
#Corresponds to specific folder name
cd uhubctl
#Navitage to specific directory
umount /media/usb-drive
#Unmount Camera - if it is mounted
uhubctl -a off -l 1-1
#Turn off power to the USB 2.0 Ports
sleep 5
echo "Turning on power to USB Ports"
uhubctl -a on -l 1-1
#Turn power back on the USB Ports
sleep 5
echo "Mounting Camera"
mount /dev/sdc1 /mnt/usb-drive #Change to logical name -Mount names change on reboot
#Remount Camera
echo "Camera is mounted under /media/usb-drive/"
cd /mnt/usb-drive/DCIM/$DATE
#Navigate to Specifc directory
#Use DATE value for specifc name of folder
echo "Copying AB.MP4 files"
find -iname '*AB.MP4' -exec cp {} /home/pi/data/ \;
#2 copies of files. AA is high quality. AB is lower quality.
echo "Finished"