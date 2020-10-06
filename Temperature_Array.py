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
    with open("/home/pi/data/Sensor_1.csv", "a") as log:
        log.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}\n".format(strftime("%Y-%m-%d %H:%M:%S"),"Sensor 1",str(die_1)+" F",str(obj_1)+" F",str(die_temp)+" C",str(obj_temp)+" C"," ","Sensor 2",str(die_2)+" F",str(obj_2)+" F",str(die_temp2)+" C",str(obj_temp2)+" C"))

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
    plt.pause(0.1)
    #write_die_temp_2(die_2)
    # graph(die_temp) - Graphing function for testing

    #print ('Object temperature: {0:0.3F}*C / {1:0.3F}*F'.format(obj_temp2, TempConversion(obj_temp2)))
    #print ('Die temperature: {0:0.3F}*C / {1:0.3F}*F'.format(die_temp2, TempConversion(die_temp2)))


