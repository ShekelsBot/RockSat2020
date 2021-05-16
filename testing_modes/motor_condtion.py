#Andrew Bruckbauer
#3/22/2021
#Motor Test Condtion Script
from time import sleep
import RPi.GPIO as GPIO
import board
from adafruit_motorkit import MotorKit
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

class Motor:

    def state1(): 
            print ("Testing Condtion 1 - ARM EXTENSION")
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
                        print ("SUBPROCESS CAMERA SCRIPT RECORD")
                        sleep (.5)
                        print ("Event 1 Test End") #call other script
                    elif kit.motor3.throttle == 0:
                        break

    def state2():
            print ("Testing Condtion 2 - ARM RETRACTION")
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
                            print ("SUBPROCESS CAMERA SCRIPT TRANSFER")
                            print ("Event 2 End")
                        elif kit.motor3.throttle == 0:
                            break

    def state3():
        print ("EXITNG MOTOR TESTING")
        print ("Button 3 Pressed")
        kit.motor3.throttle = 0 #Set throttle to zero
        #Turn off raspberry pi
        sleep(.5)
        exit

while (1):
    if (GPIO.input(button1)==0):
        state1()
    if (GPIO.input(button2)==0):
        state2()
    if (GPIO.input(button3)==0):
        state3()