#Andrew Bruckbauer
#4/4/2021
#Test Conditions

import RPi.GPIO as GPIO
import board
import subprocess
import os

GPIO.setmode(GPIO.BCM)

wire16=16
wire19=19
wire21=20

GPIO.setup(wire16,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(wire19,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(wire21,GPIO.IN,pull_up_down=GPIO.PUD_UP)

def accel():
    #os.system("cd testing_modes")
    os.system("sudo python accel_condition.py")
def temp():
    os.system("sudo python temp_array_condition.py")
def distance():
    os.system("sudo python distance_condition.py")
def motor():
    os.system("sudo python motor_condition.py")
def picamera():
    os.system("sudo python picamera_condition.py")
def cam(): 
    os.system("sudo python camera_condition.py")
def launch():
    os.system('sudo python control_2.py')

while (1):
    if (GPIO.input(wire16)==0) and GPIO.input(wire19)==1 and (GPIO.input(wire21)==1):
        print ("Condition 1")
        accel()
        break
    elif (GPIO.input(wire16)==0) and GPIO.input(wire19)==0 and (GPIO.input(wire21)==1):
        print ("Condition 2")
        temp()
        
    elif (GPIO.input(wire16)==0) and GPIO.input(wire19)==0 and (GPIO.input(wire21)==0):
        print ("Condition 3")
        picamera()
        break
    elif (GPIO.input(wire16)==1) and GPIO.input(wire19)==1 and (GPIO.input(wire21)==0):
        print ("Condition 4")
        motor()
        break
    elif (GPIO.input(wire16)==1) and GPIO.input(wire19)==0 and (GPIO.input(wire21)==0):
        print ("Condition 5")
        distance()
        break
    elif (GPIO.input(wire16)==0) and GPIO.input(wire19)==1 and (GPIO.input(wire21)==0):
        print ("Condition 6")
        cam()
        break
    elif (GPIO.input(wire16)==1) and GPIO.input(wire19)==1 and (GPIO.input(wire21)==1):
        print ("Condition 7")
        print ("LAUNCH CONDITION")
        #launch()
        break