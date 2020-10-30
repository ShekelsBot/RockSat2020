# Andrew Bruckbauer
# 11/27/2020
# Motor Testing Script
# Purpose is to ask user for throttle input - either forward stop or reverse
import time
import board
from adafruit_motorkit import MotorKit

kit = MotorKit(i2c=board.I2C())

print ("DC Motor Testing")
print ("Type one of three throttle settings")
print ("Input Throttle Command")
time.sleep(1)
print ("Forward, Stop, or Reverse")
print ("Press ENTER to exit")

while True:
    throttle = input('Command: ').lower()
    if len(throttle) == 0:
        kit.motor3.throttle = 0
        print ("EXIT success")
        break
    elif throttle in ['f','forward']:
        kit.motor3.throttle = 1
        print ('motor is moving forward')
    elif throttle in ['s','stop']:
        kit.motor3.throttle = 0
        print ('motor is stopped')
    elif throttle in ['r','reverse']:
        kit.motor3.throttle = -1
        print ('motor is in reverse')
    #elif (throttle > 1 or throttle < -1):
    #    print(throttle)
    #    print("Invalid input - throttle can only be -1 to 1.")
    elif throttle.isdigit():
        converted_throttle = int(float(throttle))
        kit.motor3.throttle = converted_throttle
        print("Throttle is "+throttle+".")
