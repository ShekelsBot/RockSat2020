#!/usr/bin/python
"""
    manualcamctl - This script manually controls the camera and is meant to 
                   be run as a standalone program.
"""

# Import dependencies
import usbcamctl
import configparser
import sys
from time import sleep
import os
from RPi import GPIO

# Load confifuration from config.ini
config = configparser.ConfigParser()
config.read('./config.ini')

#Define and setup
INHIBIT_1=int(config['pinout']['Inhibit_1'])

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Setup GPIO
GPIO.setup(INHIBIT_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Shorthand
def inhibit(id):
    if id == 1: return GPIO.input(INHIBIT_1) == 0

#Define inhibit
CAM_INHIBIT = inhibit(1)

# Main
def main(arguments):
    if "poweron" in arguments: usbcamctl.power(True)
    if "poweroff" in arguments: usbcamctl.power(False)
    if "record" in arguments: usbcamctl.toggleRecord()
    if "mode" in arguments: usbcamctl.toggleMode()
    if "usbon" in arguments: usbcamctl.usb(True)
    if "usboff" in arguments: usbcamctl.usb(False)

def camera_testing():
    usbcamctl.power(True) #Power on
    usbcamctl.usb(False) #USB Power off
    usbcamctl.toggleRecord() #Toggle recording
    sleep(10)
    usbcamctl.toggleRecord() #Stop recording
    usbcamctl.usb(True) #Turn on power to USB

    # Mount and tranfer files
    if not os.path.isdir('/mnt/usb'): os.system("sudo mkdir -p /mnt/usb")
    if not os.path.isdir('video'): os.system("mkdir video")
    sleep(2)
    os.system("sudo mount -o ro /dev/sda1 /mnt/usb")
    sleep(1)
    os.system("cp /mnt/usb/DCIM/*/*AB.MP4 ./video/")
    sleep(0.2)
    os.system("sync")
    sleep(0.2)
    os.system("sudo umount /dev/sda1")
    sleep(1)

    #Power off camera
    usbcamctl.power(False)

# Entry point
if CAM_INHIBIT:
    print ("Camera ONLY")
    camera_testing()
    if __name__ == "__main__":
        arguments = sys.argv
        arguments.pop(0)
        main(arguments)
