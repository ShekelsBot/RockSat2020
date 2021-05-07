# Control 2.0
# Andrew Bruckbauer
# 3/15/2021
# Main Control Script using Switch
# Save Function
# https://www.raspberrypi.org/forums/viewtopic.php?p=312604
# https://www.journaldev.com/15638/python-pickle-example
from time import sleep
import RPi.GPIO as GPIO
import board
import subprocess
from adafruit_motorkit import MotorKit
import pickle

GPIO.setmode(GPIO.BCM)

kit = MotorKit(i2c=board.I2C())
button1=18 #Event 1
button2=27 #Event 2
button3=22 #Event 3
limit_1=23 #Arm open
limit_2=24 #Arm closed

GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(limit_1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(limit_2,GPIO.IN,pull_up_down=GPIO.PUD_UP)

filename = 'save_state' #Name of the hex dump

def dump(): #Save state
    data = [] #data array
    raw = current_state #holder value
    data.append(raw) #add current_state to data array
    file = open ('save_state', 'wb') #open file for writing
    pickle.dump(data,file) #dump information to file
    file.close #close file

def load(): #Load State
    file = open('save_state', 'rb') #open file
    global data #global decleration for other functions
    data = pickle.load(file) #dump infomration to function
    file.close() #close file

def counter():
    cnt = 0 #iteration variable
    global item
    for item in data: #parshing loop
        print('The save state is :', item)
        cnt += 1 

def stater():
    dump() #Call data dump
    load() #Call load state
    counter() #Call counter varaible +1 to varabile

def state1(): 
        print ("Button 1 Pressed")
        print ("Arm Extension")
        sleep (.1)
        if GPIO.input(limit_2)==1: #Listen for button press
            kit.motor3.throttle = 1 #Throttle forward
            sleep (1) #Pause for limit to set
            while kit.motor3.throttle == 1: 
                if GPIO.input(limit_2)==0: #Listen for LIMIT_1 press
                    kit.motor3.throttle = 0 #Stop throttle
                    print ("Starting Camera Script RECORD")
                    sleep (.5)
                    subprocess.call("./camera_scripts/camera_control_on.sh", shell=True)
                    print ("Event 1 End") #call other script
                elif kit.motor3.throttle == 0:
                    break

def state2():
        print ("Button 2 Pressed")
        print ("Arm Retraction")
        sleep (.1)
        if GPIO.input(limit_1)==1: #Listen for button press
                kit.motor3.throttle = -1 #Reverse motor
                sleep(1) #Pause for limit to set
                print ("Camera data script TRANSFER")
                while kit.motor3.throttle == -1: 
                    if GPIO.input(limit_1)==0: #Listen for LIMIT_2 press
                        kit.motor3.throttle = 0 #Stop throttle
                        print ("Arm Closesd")
                        print ("Starting Camera Scripts")
                        subprocess.call("./camera_scripts/camera_control_off.sh", shell=True)
                        print ("Event 2 End")
                    elif kit.motor3.throttle == 0:
                        break

def state3():
    print ("Button 3 Pressed")
    print ("simulation shutdown event")
    kit.motor3.throttle = 0 #Set throttle to zero
    #Turn off raspberry pi
    sleep(.5)
    exit

load()
print ("Controler 2.0: Program Started press buttons to simulate events.")
print ("Save State Test Script")
counter()

while (1):
    if item == 0: #Save state 
        while (1): # Always run
            if (GPIO.input(button1)==0):# Listen for button press
                current_state = 1 # Save state
                stater() # update state
                state1() # State 1
            if (GPIO.input(button2)==0):
                current_state = 2 # Save state 2
                stater()
                state2() # Call state 2
            if (GPIO.input(button3)==0):
                current_state = 3
                stater()
                state3()
                current_state = 4
                stater()
                break
    elif item == 1:
        while (1):
            if (item == 1):
                current_state = 2
                stater()
                state1()
            if (GPIO.input(button2)==0):
                current_state = 2
                stater()
                state2()
            if (GPIO.input(button3)==0):
                current_state = 3
                stater()
                state3()
                current_state = 4
                stater()
                break
    elif item == 2:
        while (1):
            if (item == 2):
                current_state = 3
                stater()
                state2()
            if (GPIO.input(button3)==0):
                current_state = 3
                stater()
                state3()
                current_state = 4
                stater()
                break
    elif item == 3:
        while (1):
            if (item == 3):
                current_state = 3
                stater()
                state3()
                current_state = 4
                stater()
                break
    elif item == 4:
        current_state = 0
        dump()
        load()
        print ("Save state reset",item)
        break
    else:
        print ("greater than 4",item)
        break