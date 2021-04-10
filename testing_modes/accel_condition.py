#https://piguide.dev/2019/05/27/raspberry-pi-accelerometer-using-the-adxl345.html

import time
from time import strftime
import board
import busio
import adafruit_adxl34x
import RPi.GPIO as GPIO

i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

button1=18 #Event 1
button2=27 #Event 2
button3=22 #Event 3

GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3,GPIO.IN,pull_up_down=GPIO.PUD_UP)

def write(allAxis): #die temp file SENSOR 1
    with open("/home/pi/data/acceltest.csv", "a") as log:
        log.write("{0},{1},{2},{3},{4}\n".format(strftime("%Y-%m-%d %H:%M:%S"),"Acel",str(xAxis),str(yAxis),str(zAxis)))

xAxis = "X:" + str(round(accelerometer.acceleration[0],1))
yAxis = "Y:" + str(round(accelerometer.acceleration[1],1))
zAxis = "Z:" + str(round(accelerometer.acceleration[2],1))

def accel():
    holder = 0
    while holder <= 10:
        if holder < 10:
            # Clean up and format the reading
            allAxis = ""
            x = ("x: ","y: ","z: ")
            zipped = zip(x,accelerometer.acceleration)
            for item in zipped:
                a = item[0] + str(round(item[1],1))
                allAxis += a + "\n"
            holder = holder +1
            print ("---------------------------------")
            print ("")
            print ("Current Loop ",holder," complete.")
            print (allAxis)
            write(allAxis)
            print ("---------------------------------")
            time.sleep(1)
        else:
            print ("Test Complete")
            print ("Press Button 1 to Start")
            print ("Press Button 2 to quit")
            break

print ("ACCEL TEST STARTED")
print ("Press Button 1 to Start")
print ("Press Button 2 to quit")

while (1):
    if (GPIO.input(button1)==0):
        accel()
    if (GPIO.input(button2)==0):
        print("Testing Exited")
        break
