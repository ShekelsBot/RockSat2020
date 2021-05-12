#!/usr/bin/python
"""
    usbcamctl - This python script makes use of OS calls to uhubctl to control the camera on
                the end of the arm. (Power On/Off) (Record On/Off)

    Contributors:
        Konstantin Zaremski
        Andrew Bruckbauer

    Dependencies:
        uhubctl (installed binary) <https://github.com/mvp/uhubctl.git>
"""

# Import dependencies
import RPi.GPIO as GPIO
import asyncio
import configparser
import os

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('./config.ini')

pin = int(config['usbcamctl']['pin'])
poweron_delay = float(config['usbcamctl']['poweron_delay'])
setmode_delay = float(config['usbcamctl']['setmode_delay'])
recordon_delay = float(config['usbcamctl']['recordon_delay'])
poweroff_delay = float(config['usbcamctl']['poweroff_delay'])
recordoff_delay = float(config['usbcamctl']['recordoff_delay'])

# Setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)

# Control the camera's powered state from the USB port (uhubctl, then GPIO)
async def power(mode):
    try:
        GPIO.output(pin, GPIO.HIGH)
        asyncio.sleep(poweron_delay if mode else poweroff_delay)
        GPIO.output(pin, GPIO.LOW)
        return True
    except:
        return False

# Control the USB ports on the pi
async def usb(mode):
    try:
        os.system('sudo uhubctl -a ' + ('on' if mode else 'off') + ' -l 1-1')
        return True
    except:
        return False

# Control the camera's recording state (GPIO)
async def toggleRecord():
    try:
        GPIO.output(pin, GPIO.HIGH)
        asyncio.sleep(recordon_delay)
        GPIO.output(pin, GPIO.LOW)
        return True
    except:
        return False