from time import sleep
import RPi.GPIO as GPIO
import board
import subprocess
from adafruit_motorkit import MotorKit
GPIO.setmode(GPIO.BCM)

limit_1=23
#Arm closed switch
limit_2=24
#Arm open switch
GPIO.setup(limit_1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(limit_2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
while (1):
    if GPIO.input(limit_2)==0:
                            #kit.motor3.throttle = 0
                            print ("Limit 2 pushed")
                            sleep (.5)
    if GPIO.input(limit_1)==0:
                            #kit.motor3.throttle = 0
                            print ("Limit 1 pushed")
                            sleep (.5)