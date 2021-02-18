# Andrew Bruckbauer
# Basic test for 
from time import sleep
import RPi.GPIO as GPIO
import subprocess
GPIO.setmode(GPIO.BCM)

# The numbers count as the GPIO number not pin number
button1=18
button2=27
button3=22
GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3,GPIO.IN,pull_up_down=GPIO.PUD_UP)
while(1):
        if GPIO.input(button1)==0:
                print ("Button 1 Pressed")
                sleep(.5)
                print ("start bash sctipt")
                subprocess.call("./bingo.sh", shell=True)
        if  GPIO.input(button2)==0:
                sleep(.5)
                print ("Button 2 Pressed")
        if  GPIO.input(button3)==0:
                sleep(.5)
                print ("Button 3 Pressed")