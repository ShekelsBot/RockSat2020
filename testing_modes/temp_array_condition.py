# Andrew Bruckbauer
# 8/18/2020
# Temperature Sensor Module
# Purpose of the code is to create a temp sensor
# https://learn.adafruit.com/tmp006-temperature-sensor-python-library/software
# TMP006 Adafruit Module

from time import sleep, strftime, time
import Adafruit_TMP.TMP006 as TMP006
import RPi.GPIO as GPIO
import board
import busio

GPIO.setmode(GPIO.BCM)
i2c = busio.I2C(board.SCL, board.SDA)

button1=18 #Event 1
button2=27 #Event 2
button3=22 #Event 3

GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3,GPIO.IN,pull_up_down=GPIO.PUD_UP)

# Function to convert celsius (c) to fahrenhiet.
def TempConversion(c):
    return c * 9.0 / 5.0 + 32

def write_die_temp(): #die temp file SENSOR 1
    with open("/home/pi/data/Sensor_1.csv", "a") as log:
        log.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}\n".format(strftime("%Y-%m-%d %H:%M:%S"),"Sensor 1",str(die_1)+" F",str(obj_1)+" F",str(die_temp)+" C",str(obj_temp)+" C"," ","Sensor 2",str(die_2)+" F",str(obj_2)+" F",str(die_temp2)+" C",str(obj_temp2)+" C"))

# Initialze sensor
sensor = TMP006.TMP006()
sensor_2 = TMP006.TMP006()

#i2c = busio.I2C(board.SCL, board.SDA)
sensor = TMP006.TMP006(address=0x40, busnum=1) # Default i2C address is 0x40 and bus is 1.
sensor_2 = TMP006.TMP006(address=0x41, busnum =1) # change 3v to ad0

# Default rate is 16 samples per loop.
sensor.begin()
sensor_2.begin()
# Loop printing measurements every second.

def temparray():
    holder = 0
    while holder <= 10:
        if holder < 10:
            global die_temp, die_1, obj_temp, obj_1
            global die_temp2, die_2, obj_temp2, obj_2
            die_temp = sensor.readDieTempC()
            die_1 = TempConversion(die_temp)
            obj_temp = sensor.readObjTempC()
            obj_1 = TempConversion(obj_temp)

            die_temp2 = sensor_2.readDieTempC()
            die_2 = TempConversion(die_temp2)
            obj_temp2 = sensor_2.readObjTempC()
            obj_2= TempConversion(obj_temp2)
            
            holder = holder +1
            print ("---------------------------------")
            print ("")
            print ("Current Loop ",holder," complete.")
            print ("Sensor 1:",die_1,"Farenheit")
            print ("Sensor 1:",die_2,"Farenheit")
            write_die_temp()
            print ("---------------------------------")
            sleep (1)
        else:
            print ("Test Complete")
            print ("Press Button 1 to Start")
            print ("Press Button 2 to quit")
            break

print ("TEMP_ARRAY TEST STARTED")
print ("Press Button 1 to Start")
print ("Press Button 2 to quit")

while (1):
    if (GPIO.input(button1)==0):
        #write_die_temp()
        temparray()
    if (GPIO.input(button2)==0):
        print("Testing Exited")
        break



