# Andrew Bruckbauer
# 12/11/2020
# Telemetry Module 3.0
# Combines all modules
# Check DEF sensors for wiring

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
# https://iot4beginners.com/how-to-read-and-write-from-serial-port-using-raspberry-pi/
# https://www.devdungeon.com/content/how-connect-serial-console

# TMP006 Adafruit Module
# vl53l0x Distance Sesnor
# adxl34x Accelerometer
# Adafruit Motor Hat
# Pi Camera

from multiprocessing import Process
import board, busio, os, serial
import time
from time import strftime
import Adafruit_TMP.TMP006 as TMP006
import adafruit_vl53l0x
import adafruit_adxl34x

i2c = busio.I2C(board.SCL, board.SDA)

'''
# Define serial port
ser = serial.Serial(
        port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
'''
def TempConversion(c):
    return c * 9.0 / 5.0 + 32

def write_sensors(): 
    with open("/home/pi/data/Telemetry.csv", "a") as log:
        log.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},\n"
        .format(strftime("%Y-%m-%d %H:%M:%S"),"Temp1",str(TempConversion(die1))+" F",str(TempConversion(obj1))+" F",str(die1)+" C",str(obj1)+" C",
        " ","Distance","BLANK MM"
        ,str(xAxis),str(yAxis),str(zAxis)))

def sensors():
    # Temperature Sensor 1
    # VCC - RED - 3.5v
    # GND - BLK - Ground
    # SDA - YLW - SDA
    # SCL - BRN - SCL
    sensor1 = TMP006.TMP006()
    sensor1 = TMP006.TMP006(address=0x40, busnum=1) # Default i2C address is 0x40 and bus is 1.
    sensor1.begin()
    # Accelerometer Sensor
    # 3v3 - RED - 3.5v
    # GND - BLK - Ground
    # SDA - YLW - SDA
    # SCL - BRN - SCL
    accelerometer = adafruit_adxl34x.ADXL345(i2c)
    # Distance Sensor
    # VIN - RED - 3.5v
    # GND - BLK - Ground
    # SDA - YLW - SDA
    # SCL - BRN - SCL
    vl53 = adafruit_vl53l0x.VL53L0X(i2c)

    while True:
        # Distance Sensor
        global distance
        distance = vl53.range
        print ("Range: {0}mm".format(distance))
        #ser.write (b'Range: %d '%(distance)+b' mm \n')
        time.sleep(.1)

        # Temperature Sensor 1
        global obj1
        global die1
        obj1 = sensor1.readObjTempC()
        die1 = sensor1.readDieTempC()

        # Temperature Sensor 1 Serial out
        #ser.write (b'Sensor 1 object Temperature: %d \n'%(obj1))
        #ser.write (b'Sensor 1 die Temperature: %d \n'%(die1))
        print ('Object temperature: {0:0.3F}*C / {1:0.3F}*F'.format(obj1, TempConversion(obj1)))
        print ('Die temperature: {0:0.3F}*C / {1:0.3F}*F'.format(die1, TempConversion(die1)))
        time.sleep(.1)

        # Accelerometer tupple parse
        global xAxis
        global yAxis
        global zAxis
        xAxis = (round(accelerometer.acceleration[0],1))
        yAxis = (round(accelerometer.acceleration[1],1))
        zAxis = (round(accelerometer.acceleration[2],1))

        '''
        # Accelerometer Serial out
        ser.write (b'X Axis: %d \n'%(xAxis))
        ser.write (b'Y Axis: %d \n'%(yAxis))
        ser.write (b'Z Axis: %d \n'%(zAxis))
        '''

        print ('X Axis: %d \n'%(xAxis))
        print ('Y Axis: %d \n'%(yAxis))
        print ('Z Axis: %d \n'%(zAxis))
        
        #Write all data
        write_sensors()
        time.sleep(1)

# Loop printing measurements every second.
# Tell where stuff is being stored
print ('Press Ctrl-C to quit.')
print ('Storing data /home/pi/data')
print ('Temperature is in Fahrenheit')
print ('Distance is in MM')
    
# Multiprocess start loop
if __name__=='__main__':
    p1 = Process(target = sensors)
    p1.start()