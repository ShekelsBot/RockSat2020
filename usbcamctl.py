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
from time import sleep
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
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)

# Control the camera's powered state from the USB port (uhubctl, then GPIO)
def power(mode):
    try:
        GPIO.output(pin, GPIO.HIGH)
        sleep(poweron_delay if mode else poweroff_delay)
        GPIO.output(pin, GPIO.LOW)
        sleep(5)
        return True
    except:
        return False

# Control the USB ports on the pi
def usb(mode):
    try:
        output = os.system('sudo uhubctl -a ' + ('on' if mode else 'off') + ' -l 1-1 > /dev/null')
        sleep(3)
        return True
    except:
        return False

# Control the camera's recording state (GPIO)
def toggleRecord():
    try:
        GPIO.output(pin, GPIO.HIGH)
        sleep(recordon_delay)
        GPIO.output(pin, GPIO.LOW)
        sleep(3)
        return True
    except:
        return False

# Toggle the camera's mode (GPIO)
def toggleMode():
    try:
        GPIO.output(pin, GPIO.HIGH)
        sleep(setmode_delay)
        GPIO.output(pin, GPIO.LOW)
        sleep(3)
        return True
    except:
        return False