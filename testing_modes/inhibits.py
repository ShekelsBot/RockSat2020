# Andrew Bruckbauer
# Inhibits Testing
# 
'''
-_-_-_-_-Testing Codes-_-_-_-_-
Condition 1 (Accel)    16 0 0 
Condition 2 (Temp)     16 19 0
Condition 3 (Pi Cam)   19 19 20
Condition 4 (Motor)    0 0 21
Condition 5 (Distance) 0 19 21
Condition 6 (Cam)      16 0 21
Condition 7 (Launch)   0 0 0
-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
'''

import RPi.GPIO as GPIO
import board
import subprocess
import os
from adafruit_motorkit import MotorKit

# Unique
from logger import Logger
import usbcamctl
import persist
from accel_condition import Accel
from camera_condition import Camera
from distance_condition import Distance

# Load confifuration from config.ini
config = configparser.ConfigParser()
config.read('./config.ini')

#Define and setup
INHIBIT_1=int(config['Inhibit_1'])
INHIBIT_2=int(config['Inhibit_2'])
INHIBIT_3=int(config['Inhibit_3'])

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Setup GPIO
GPIO.setup(INHIBIT_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(INHIBIT_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(INHIBIT_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Shorthand
def inhibit(id):
    if id == 1 return: GPIO.input(INHIBIT_1) == 0
    if id == 2 return: GPIO.input(INHIBIT_2) == 0
    if id == 3 return: GPIO.input(INHIBIT_3) == 0

# Define inhibit conditions based on evaluation of pin states
ACCEL_INHIBIT = inhibit(1)
TEMP_INHIBIT = inhibit(1) and inhibit(2)
PICAMERA_INHIBIT = inhibit(1) and inhibit(2) and inhibit(3)
MOTOR_INHIBIT = inhibit(3)
DISTANCE_INHIBIT = inhibit(2) and inhibit(3)
CAM_INHIBIT = inhibit(1) and inhibit(3)  

#Listen for timer events or testing mode
EXTERNAl_TRIGGER = True

# Set GPIO mode
GPIO.setmode(GPIO.BCM)
#MotorKit class
kit = MotorKit(i2c=board.I2C())
arm = kit.motor3

def accel_test():
    print("Accel Test")
    Accel()
def temp_test():
    print("Temp Test")
def picamera_test():
    print ("Pi Cam Test")

def motor_test():
    print ("Motor Test")

def distance_test():
    print ("Distance Test")
    Distance()
    
def cam_test():
    print ("Camera Test")
    Camera()
    
while (1):
    if ACCEL_INHIBIT: accel_test()
    if TEMP_INHIBIT: temp_test()
    if PICAMERA_INHIBIT: picamera_test()
    if MOTOR_INHIBIT: motor_test()
    if DISTANCE_INHIBIT: distance_test()
    if CAM_INHIBIT: cam_test()