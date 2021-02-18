# Uses modifed selfie stick circut
# Make sure camera is set in camera mode
# Switches from one mode to another
# Change record time
import RPi.GPIO as GPIO
import time

pin = 33
power_on_seconds = 2
set_mode_seconds = 1
record_on_seconds = .5
power_off_seconds = 4
record_time_seconds = 10

time_delay1 = 3
time_delay2 = 8

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)

#Recording set
print("Recording On.")
GPIO.output(pin, GPIO.HIGH)
time.sleep(record_on_seconds)
GPIO.output(pin, GPIO.LOW)

#Time to record:
time.sleep(record_time_seconds)

print("Recording Off.")
GPIO.output(pin, GPIO.HIGH)
time.sleep(record_on_seconds)
GPIO.output(pin, GPIO.LOW)
