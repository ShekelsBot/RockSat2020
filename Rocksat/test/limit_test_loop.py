from time import sleep
import RPi.GPIO as GPIO
import board
import subprocess
from adafruit_motorkit import MotorKit
GPIO.setmode(GPIO.BCM)

kit = MotorKit(i2c=board.I2C())
button1=18
button2=27
button3=22

limit_1=23
#Arm closed switch
limit_2=24
#Arm open switch

GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3,GPIO.IN,pull_up_down=GPIO.PUD_UP)
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

    if GPIO.input(button1)==0:
                    print ("Button 1 Pressed")
                    print ("Arm Extension")
                    sleep (.1)
                    if GPIO.input(limit_2)==1:
                        kit.motor3.throttle = 1
                        sleep (1)
                        while kit.motor3.throttle == 1:
                            if GPIO.input(limit_2)==0:
                                print ('in IF Statement')
                                kit.motor3.throttle = 0
                                print ("Starting Camera Script RECORD")
                                sleep (.5)
                                subprocess.call("./camera_scripts/camera_control_on.sh", shell=True)
                                print ("other scripts")
                                #call other script
                            elif kit.motor3.throttle == 0:
                                break
    if  GPIO.input(button2)==0:
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
                                print ("arm closed")
                                print ("starting camera scripts")
                                subprocess.call("./camera_scripts/camera_control_off.sh", shell=True)
                            elif kit.motor3.throttle == 0:
                                break

                        #call other script
    if  GPIO.input(button3)==0:
                    print ("Button 3 Pressed")
                    print ("simulation shutdown event")
                    kit.motor3.throttle = 0
                    #Turn off raspberry pi
                    sleep(.5)
                    break