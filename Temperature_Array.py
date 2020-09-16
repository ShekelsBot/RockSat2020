# Andrew Bruckbauer
# 8/18/2020
# Temperature Sensor Module
# Purpose of the code is to create a temp sensor
# https://learn.adafruit.com/tmp006-temperature-sensor-python-library/software
# TMP006 Adafruit Module

from time import sleep, strftime, time
import matplotlib.pyplot as plt
import Adafruit_TMP.TMP006 as TMP006

plt.ion()
x = []
y = []

# Function to convert celsius (c) to fahrenhiet.
def TempConversion(c):
    return c * 9.0 / 5.0 + 32

def write_die_temp(die_1): #die temp file SENSOR 1
    with open("/home/pi/data/die_temp.csv", "a") as log:
        log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(die_1)))
def write_obj_temp(obj_1): #obj temp file SENSOR 2
    with open("/home/pi/data/obj_temp.csv", "a") as log:
        log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(obj_1)))

def write_die_temp_2(die_2): #obj temp file SENSOR 2
    with open("/home/pi/data/die_temp_2.csv", "a") as log:
        log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(die_2)))
def write_obj_temp_2(obj_2): #obj temp file SENSOR 2
    with open("/home/pi/data/obj_temp_2.csv", "a") as log:
        log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(obj_2)))

def graph(temp):
    y.append(temp)
    x.append(time())
    plt.clf()
    plt.scatter(x,y)
    plt.plot(x,y)
    plt.draw()

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
print ('Press Ctrl-C to quit.')
print ('Storing data /home/pi/data')
print ('Temperature is in Fahrenheit')


while True:

    die_temp = sensor.readDieTempC()
    die_1 = TempConversion(die_temp)
    obj_temp = sensor.readObjTempC()
    obj_1 = TempConversion(obj_temp)

    die_temp2 = sensor_2.readDieTempC()
    die_2 = TempConversion(die_temp2)
    obj_temp2 = sensor_2.readObjTempC()
    obj_2= TempConversion(obj_temp2)

    #print ('Object temperature: {0:0.3F}*C / {1:0.3F}*F'.format(obj_temp, TempConversion(obj_temp)))
    #print ('Die temperature: {0:0.3F}*C / {1:0.3F}*F'.format(die_temp, TempConversion(die_temp)))

    write_die_temp(die_1)
    write_obj_temp(obj_1)
    # graph(die_temp) - Graphing function for testing
    plt.pause(1)

    #print ('Object temperature: {0:0.3F}*C / {1:0.3F}*F'.format(obj_temp2, TempConversion(obj_temp2)))
    #print ('Die temperature: {0:0.3F}*C / {1:0.3F}*F'.format(die_temp2, TempConversion(die_temp2)))

    write_die_temp_2(die_2)
    write_obj_temp_2(obj_2)
    plt.pause(2)

