# Control 2.0
# Andrew Bruckbauer
# 3/15/2021
# Main Control Script using Switch
# Save Function
# https://www.raspberrypi.org/forums/viewtopic.php?p=312604
from time import sleep
import RPi.GPIO as GPIO
import board
import subprocess
from adafruit_motorkit import MotorKit
import pickle

GPIO.setmode(GPIO.BCM)

kit = MotorKit(i2c=board.I2C())
button1=18
#Event 1
button2=27
#Event 2
button3=22
#Event 3
limit_1=23
#Arm open
limit_2=24
#Arm closed

GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(limit_1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(limit_2,GPIO.IN,pull_up_down=GPIO.PUD_UP)

filename = 'save_state'

def dump():
    data = []
    raw = current_state 
    data.append(raw)
    file = open ('save_state', 'wb')
    pickle.dump(data,file)
    file.close

def load():
    file = open('save_state', 'rb')
    global data
    data = pickle.load(file)
    file.close()

def counter():
    cnt = 0
    for item in data:
        print('The save state is : ', item)
        cnt += 1

def state1():
        print ("Button 1 Pressed")
        print ("Arm Extension")
        sleep (.1)
        if GPIO.input(limit_2)==1:
            kit.motor3.throttle = 1
            sleep (1)
            while kit.motor3.throttle == 1:
                if GPIO.input(limit_2)==0:
                    kit.motor3.throttle = 0
                    print ("Starting Camera Script RECORD")
                    sleep (.5)
                    subprocess.call("./camera_scripts/camera_control_on.sh", shell=True)
                    print ("Event 1 End")
                    #call other script
                    break
                elif kit.motor3.throttle == 0:
                    break

def state2():
        print ("Button 2 Pressed")
        print ("Arm Retraction")
        #kit.motor3.throttle = -1
        if GPIO.input(limit_1)==1:
                kit.motor3.throttle = -1
                sleep(.5)
                print ("Camera data script TRANSFER")
                while kit.motor3.throttle == -1:
                    if GPIO.input(limit_1)==0:
                        kit.motor3.throttle = 0
                        print ("Arm Closesd")
                        print ("Starting Camera Scripts")
                        subprocess.call("./camera_scripts/camera_control_off.sh", shell=True)
                        print ("Event 2 End")
                    elif kit.motor3.throttle == 0:
                        break

def state3():
    print ("Button 3 Pressed")
    print ("simulation shutdown event")
    kit.motor3.throttle = 0
    #Turn off raspberry pi
    sleep(.5)
    exit

load()
print ("Controler 2.0: Program Started press buttons to simulate events.")
print ("Save State Test Script")
counter()

while (1):
    if (GPIO.input(button1)==0):
        current_state = 1

        dump()
        load()
        counter()
        state1()
    if (GPIO.input(button2)==0):
        current_state = 2

        dump()
        load()
        counter()
        state2()
    if (GPIO.input(button3)==0):
        current_state = 3

        dump()
        load()
        counter()
        state3()
        break
print("State = ",current_state)
# Pause
sleep(1)