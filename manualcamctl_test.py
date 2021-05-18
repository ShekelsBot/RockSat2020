#!/usr/bin/python
"""
    manualcamctl - This script manually controls the camera and is meant to 
                   be run as a standalone program.
"""
# Import dependencies
import usbcamctl
import sys

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

# Entry point
'''
if __name__ == "__main__":
    arguments = sys.argv
    arguments.pop(0)
    main(arguments)

'''
if CAM_INHIBIT:
    if __name__ == "__main__":
    arguments = sys.argv
    arguments.pop(0)
    main(arguments)
