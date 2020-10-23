#https://piguide.dev/2019/05/27/raspberry-pi-accelerometer-using-the-adxl345.html

import time
from time import strftime
import board
import busio
import adafruit_adxl34x
import matplotlib.pyplot as plt

i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

accelerometer.enable_motion_detection()

def write(data): #die temp file SENSOR 1
    with open("/home/pi/data/acceltest", "a") as log:
        log.write("{0},{1},{2},\n".format(strftime("%Y-%m-%d %H:%M:%S"),"Sensor 1",str(data)))


while True:
    data = ("%f %f %f"%accelerometer.acceleration)
    #print("%f %f %f"%accelerometer.acceleration)
    print (data)
    print("%s" % accelerometer.events["motion"])
    write(data)
    plt.pause(1)