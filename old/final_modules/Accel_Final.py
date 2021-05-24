#https://piguide.dev/2019/05/27/raspberry-pi-accelerometer-using-the-adxl345.html

import time
from time import strftime
import board
import busio
import adafruit_adxl34x

i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

def write(allAxis): #die temp file SENSOR 1
    with open("/home/pi/data/acceltest.csv", "a") as log:
        log.write("{0},{1},{2},{3},{4}\n".format(strftime("%Y-%m-%d %H:%M:%S"),"Acel",str(xAxis),str(yAxis),str(zAxis)))

xAxis = "X:" + str(round(accelerometer.acceleration[0],1))
yAxis = "Y:" + str(round(accelerometer.acceleration[1],1))
zAxis = "Z:" + str(round(accelerometer.acceleration[2],1))

while True:
    # Clean up and format the reading
    allAxis = ""
    x = ("x: ","y: ","z: ")
    zipped = zip(x,accelerometer.acceleration)
    for item in zipped:
        a = item[0] + str(round(item[1],1))
        allAxis += a + "\n"
    print (allAxis)
    time.sleep(1)
