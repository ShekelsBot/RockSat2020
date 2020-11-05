# Andrew Bruckbauer
# 8/18/2020
# Temperature Sensor Module
# Purpose of the code is to create a temp sensor
# https://learn.adafruit.com/tmp006-temperature-sensor-python-library/software
# TMP006 Adafruit Module

import time
import serial
import Adafruit_TMP.TMP006 as TMP006

# Define serial port
ser = serial.Serial(
        port='/dev/ttyAMA0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

# Function to convert celsius (c) to fahrenhiet.
def TempConversion(c):
    return c * 9.0 / 5.0 + 32

# Initialze sensor
sensor = TMP006.TMP006()

# Default i2C address is 0x40 and bus is 1.
sensor = TMP006.TMP006(address=0x40, busnum=1)

# Default rate is 16 samples per loop.
sensor.begin()

# Loop printing measurements every second.
print ('Press Ctrl-C to quit.')
while True:
    obj_temp = sensor.readObjTempC()
    die_temp = sensor.readDieTempC()
    #reads object temp
    print ('Object temperature: {0:0.3F}*C / {1:0.3F}*F'.format(obj_temp, TempConversion(obj_temp)))
    #reads die temp
    print ('Die temperature: {0:0.3F}*C / {1:0.3F}*F'.format(die_temp, TempConversion(die_temp)))
    time.sleep(1.0)

    #Sends data over seial connection
    ser.write("Serial Connection: OBJ temperature is: {0:0.3F}*C / {1:0.3F}*F".format(obj_temp, TempConversion(obj_temp)))
    ser.write("Serial Connection: DIE temperature is: {0:0.3F}*C / {1:0.3F}*F".format(die_temp, TempConversion(die_temp)))
    time.sleep(1)
