# Andrew Bruckbauer
# 8/18/2020
# Main Telelmetry model
# Combines all previous iterations of code from the repository to create one module.

# Documentation on sensors
# https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
# https://learn.adafruit.com/tmp006-temperature-sensor-python-library/software
# https://learn.adafruit.com/adafruit-vl53l0x-micro-lidar-distance-sensor-breakout/python-circuitpython
# https://piguide.dev/2019/05/27/raspberry-pi-accelerometer-using-the-adxl345.html
# https://circuitpython.readthedocs.io/projects/motorkit/en/latest/
# https://learn.adafruit.com/i2c-addresses/the-list

# pip3 install picamera
# pip3 install psutil

# mkdir videos
# mkdir data

# Serial Connection Documentation
# https://www.engineersgarage.com/raspberrypi/articles-raspberry-pi-serial-communication-uart-protocol-ttl-port-usb-serial-boards/
# https://www.devdungeon.com/content/how-connect-serial-console

# TMP006 Adafruit Module
# vl53l0x Distance Sesnor
# adxl34x Accelerometer
# Adafruit Motor Hat
# Pi Camera

import time
from time import strftime
import board
import busio
import Adafruit_TMP.TMP006 as TMP006
import adafruit_vl53l0x
import adafruit_adxl34x
import picamera
import os
import psutil

MAX_FILES = 999
DURATION = 20
SPACE_LIMIT = 80
TIME_STATUS_OK = 0.5

file_root = "/home/pi/videos/"

# Initialze sensors
# Initilize i2c bus and distance sensor
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# Function to convert celsius (c) to fahrenhiet.
def TempConversion(c):
    return c * 9.0 / 5.0 + 32

# Function to write data to a .csv file for graphing
def write_sensors(die_1): 
    with open("/home/pi/data/Telemetry.csv", "a") as log:
        log.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17}\n"
        .format(strftime("%Y-%m-%d %H:%M:%S"),"Sensor 1",str(die_1)+" F",str(obj_1)+" F",str(die_temp)+" C",str(obj_temp)+" C",
        " ","Sensor 2",str(die_2)+" F",str(obj_2)+" F",str(die_temp2)+" C",str(obj_temp2)+" C"," ","Sensor 3",str(distance)+" MM"
        ,str(xAxis),str(yAxis),str(zAxis)))

# Define both Temp Sensors
sensor = TMP006.TMP006()
sensor_2 = TMP006.TMP006()
# Address both Temp Sensors
sensor = TMP006.TMP006(address=0x40, busnum=1) # Default i2C address is 0x40 and bus is 1.
sensor_2 = TMP006.TMP006(address=0x41, busnum =1) # change 3v to ad0

# Default rate is 16 samples per loop.
# Initilize both Temp Sensors
sensor.begin()
sensor_2.begin() 

# Loop printing measurements every second.
# Tell where stuff is being stored
print ('Press Ctrl-C to quit.')
print ('Storing data /home/pi/data')
print ('Temperature is in Fahrenheit')
print ('Distance is in MM')

"""
if(psutil.disk_usage(".").percent > SPACE_LIMIT):
    print('WARNING: Low space!')
    exit()

with picamera.PiCamera() as camera:
    camera.resolution = (1920,1080)
    camera.framerate = 30

    print('Searching files...')
    for i in range(1, MAX_FILES):
        file_number = i
        file_name = file_root + "video" + str(i).zfill(3) + ".h264"
        exists = os.path.isfile(file_name)
        if not exists:
            print ("Search Complete")
            break

    for file_name in camera.record_sequence(file_root + "video%03d.h264" % i for i in range(file_number, MAX_FILES)):
        timeout = time.time() + DURATION
        print('Recording to %s' % file_name)

        while(time.time() < timeout):
            time.sleep(TIME_STATUS_OK)
            if(psutil.disk_usage(".").percent > SPACE_LIMIT):
                print('WARNING: Low space!')
                break;
"""
# Main loop
while True:

    # Variable Juggling for Temp Sensor 1
    die_temp = sensor.readDieTempC()
    die_1 = TempConversion(die_temp)
    obj_temp = sensor.readObjTempC()
    obj_1 = TempConversion(obj_temp)

    # Variable Juggling for Temp Sensor 2
    die_temp2 = sensor_2.readDieTempC()
    die_2 = TempConversion(die_temp2)
    obj_temp2 = sensor_2.readObjTempC()
    obj_2= TempConversion(obj_temp2)

    # Distance variable setup
    distance = vl53.range

    # Parse tuple for various axis
    xAxis = "X:" + str(round(accelerometer.acceleration[0],1))
    yAxis = "Y:" + str(round(accelerometer.acceleration[1],1))
    zAxis = "Z:" + str(round(accelerometer.acceleration[2],1))

    # Print statements for the main sensors 
    print ('Object temperature: {0:0.3F}*C / {1:0.3F}*F'.format(obj_temp, TempConversion(obj_temp)))
    print ('Object temperature: {0:0.3F}*C / {1:0.3F}*F'.format(obj_temp2, TempConversion(obj_temp2)))
    print("Range: {0}mm".format(vl53.range))
    
    # Clean up and format the reading
    # Create indivudal strngs from tuple data
    allAxis = ""
    x = ("x: ","y: ","z: ")
    zipped = zip(x,accelerometer.acceleration)
    for item in zipped:
        a = item[0] + str(round(item[1],1))
        allAxis += a + "\n"
    print (allAxis)

    # Write data
    write_sensors(die_1)
    time.sleep(1)
