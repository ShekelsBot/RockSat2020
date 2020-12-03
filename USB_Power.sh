#!/bin/bash
umount /media/usb-drive
uhubctl -a off -l 1-1
sleep 5
echo "Turning on power to USB Ports"
uhubctl -a on -l 1-1
sleep 5
echo "Mounting Camera"
mount /dev/sda1 /mnt/usb-drive
echo "All done"