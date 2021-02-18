# Andrew Bruckbauer
# 
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
button1=18
button2=27
button3=22
GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#GPIO.setup(button2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#GPIO.setup(button3,GPIO.IN,pull_up_down=GPIO.PUD_UP)
while(1):
        if GPIO.input(button1)==0:
                print ("Button 1 Pressed")
                sleep(.1)
        #if  GPIO.input(button2)==0:
        #        sleep(.1)
        #        print ("Button 2 Pressed")
        #if  GPIO.input(button3)==0:
        #        sleep(.1)
        #        print ("Button 3 Pressed")