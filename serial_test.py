import serial
serialport = serial.Serial("/dev/ttyS0", 9600, timeout=0.5)
serialport.write("What you want to send")
response = serialport.readlines(None)
print response