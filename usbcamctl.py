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
import configparser
import os
import time

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('./config.ini')

pin = int(config['usbcamctl']['pin'])
poweron_delay = int(config['usbcamctl']['poweron_delay'])
setmode_delay = int(config['usbcamctl']['setmode_delay'])
recordon_delay = int(config['usbcamctl']['recordon_delay'])
poweroff_delay = int(config['usbcamctl']['poweroff_delay'])
recordoff_delay = int(config['usbcamctl']['recordoff_delay'])

# Setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)

# Control the camera's powered state from the USB port (uhubctl, then GPIO)
def power(mode):
    try:
        if mode:
            os.system('sudo uhubctl -a off -l 1-1')
            time.sleep(3)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(poweron_delay if mode else poweroff_delay)
        GPIO.output(pin, GPIO.LOW)
        return true
    except:
        return false

# Control the camera's recording state (GPIO)
def toggleRecord():
    try:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(record_on_seconds)
        GPIO.output(pin, GPIO.LOW)
        return true
    except:
        return false