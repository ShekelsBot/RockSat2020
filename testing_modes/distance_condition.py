# Andrew Bruckbauer
# 8/22/2020
# Distance Sensor Module
# Purpose of the code is to create a distance sensor
# https://learn.adafruit.com/adafruit-vl53l0x-micro-lidar-distance-sensor-breakout/python-circuitpython
# See the example here for more details:
# https://github.com/pololu/vl53l0x-arduino/blob/master/examples/Single/Single.ino
# VL53L0X Adafruit Module

# Will print the sensed range/distance every second.
from time import sleep, strftime, time
import board
import busio
import adafruit_vl53l0x
import RPI.GPIO as GPIO

class Disance:

    # Initialize I2C bus and sensor.
    i2c = busio.I2C(board.SCL, board.SDA)
    vl53 = adafruit_vl53l0x.VL53L0X(i2c)

    # Main loop will read the range and print it every second. and record it
    def distance_loop():
        holder = 0
        while holder <= 10:
            if holder < 10:
                global distance
                distance = vl53.range

                holder = holder +1
                print ("---------------------------------")
                print ("")
                print("Range: {0}mm".format(vl53.range))
                print ("Loop "+holder+" complete.")
                print ("---------------------------------")
                sleep(1)
            else:
                print ("Test Complete")
                print ("Press Button 1 to Start")
                print ("Press Button 2 to quit")
                break

    print ("DISTANCE TEST STARTED")

