# Andrew Bruckbauer
# 8/18/2020
# Temperature Sensor Module
# Purpose of the code is to create a temp sensor
# https://learn.adafruit.com/tmp006-temperature-sensor-python-library/software
# TMP006 Adafruit Module

#from time import sleep, strftime, time
import time
import matplotlib.pyplot as plt
import board
import busio
import Adafruit_TMP.TMP006 as TMP006
import adafruit_vl53l0x
import picamera
import os
import psutil

MAX_FILES = 999
DURATION = 20
SPACE_LIMIT = 80
TIME_STATUS_OK = 0.5

file_root = "/home/pi/videos/"

# Function to convert celsius (c) to fahrenhiet.
def TempConversion(c):
    return c * 9.0 / 5.0 + 32

# Write for all sensors
def write_die_temp(die_1): 
    with open("/home/pi/data/Telemetry.csv", "a") as log:
        log.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14}\n"
        .format(strftime("%Y-%m-%d %H:%M:%S"),"Sensor 1",str(die_1)+" F",str(obj_1)+" F",str(die_temp)+" C",str(obj_temp)+" C",
        " ","Sensor 2",str(die_2)+" F",str(obj_2)+" F",str(die_temp2)+" C",str(obj_temp2)+" C"," ","Sensor 3",str(distance)+" MM"))

# Initialze sensors
# Initilize i2c bus and distance sensor
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)
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
print ('Press Ctrl-C to quit.')
print ('Storing data /home/pi/data')
print ('Temperature is in Fahrenheit')
print ('Distance is in MM')

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
    # Write data
    write_die_temp(die_1)
    plt.pause(1)