# Andrew Bruckbauer
# 4/30/2021
# Control Script 3 for final integration testing

from time import sleep
import RPi.GPIO as GPIO
import board
import subprocess
from adafruit_motorkit import MotorKit
import pickle

GPIO.setmode(GPIO.BCM)

kit = MotorKit(i2c=board.I2C())

button1=18 
GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

while (1):
    while (GPIO.input(button1)==1):
        print ("Connection Made")