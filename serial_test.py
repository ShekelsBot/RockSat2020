import time
import serial

print('a write')       
      
ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
           )
counter=0

ser.write('write')
print('a write')
      
while 1:
    ser.write('Write counter: %d \n'%(counter))
    print('Write counter: %d \n'%(counter))
    time.sleep(1)
    counter += 1