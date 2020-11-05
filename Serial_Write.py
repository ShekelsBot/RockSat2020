# https://iot4beginners.com/how-to-read-and-write-from-serial-port-using-raspberry-pi/
#!/usr/bin/env python
import time
import serial
ser = serial.Serial(
        port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
counter=0
while 1: 
    ser.write(b'Write counter: %d \n'%(counter)) #encode to bytes
    time.sleep(1) 
    counter += 1