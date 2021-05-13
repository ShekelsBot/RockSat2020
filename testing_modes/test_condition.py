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
wire20=20

'''
-_-_-_-_-Testing Codes-_-_-_-_-
Condition 1 (Accel)    16 0 0 
Condition 2 (Temp)     16 19 0
Condition 3 (Pi Cam)   16 19 21
Condition 4 (Motor)    0 0 21
Condition 5 (Distance) 0 19 21
Condition 6 (Cam)      16 0 21
Condition 7 (Launch)   0 0 0
-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
'''

GPIO.setup(wire16,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(wire19,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(wire20,GPIO.IN,pull_up_down=GPIO.PUD_UP)

print("-_-_-_-_-Testing Codes-_-_-_-_-")
print("Condition 1 (Accel)    16 0 0 ")
print("Condition 2 (Temp)     16 19 0")
print("Condition 3 (Pi Cam)   16 19 21")
print("Condition 4 (Motor)    0 0 21")
print("Condition 5 (Distance) 0 19 21")
print("Condition 6 (Cam)      16 0 21")
print("Condition 7 (Launch)   0 0 0")
print("-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-")

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
    if (GPIO.input(wire16)==0) and GPIO.input(wire19)==1 and (GPIO.input(wire20)==1):
        print ("Condition 1")
        accel()
        break
    elif (GPIO.input(wire16)==0) and GPIO.input(wire19)==0 and (GPIO.input(wire20)==1):
        print ("Condition 2")
        temp()
        
    elif (GPIO.input(wire16)==0) and GPIO.input(wire19)==0 and (GPIO.input(wire20)==0):
        print ("Condition 3")
        picamera()
        break
    elif (GPIO.input(wire16)==1) and GPIO.input(wire19)==1 and (GPIO.input(wire20)==0):
        print ("Condition 4")
        motor()
        break
    elif (GPIO.input(wire16)==1) and GPIO.input(wire19)==0 and (GPIO.input(wire20)==0):
        print ("Condition 5")
        distance()
        break
    elif (GPIO.input(wire16)==0) and GPIO.input(wire19)==1 and (GPIO.input(wire20)==0):
        print ("Condition 6")
        cam()
        break
    elif (GPIO.input(wire16)==1) and GPIO.input(wire19)==1 and (GPIO.input(wire20)==1):
        print ("Condition 7")
        print ("LAUNCH CONDITION")
        #launch()
        break
