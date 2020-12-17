# Uses modifed selfie stick circut
# Shuts off power
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

print("Recording Off.")
GPIO.output(pin, GPIO.HIGH)
time.sleep(record_on_seconds)
GPIO.output(pin, GPIO.LOW)

time.sleep(time_delay1)
"""
print("Setting to Default.")
GPIO.output(pin, GPIO.HIGH)
time.sleep(set_mode_seconds)
GPIO.output(pin, GPIO.LOW)

time.sleep(time_delay1)
"""
print("Turning Off.")
GPIO.output(pin, GPIO.HIGH)
time.sleep(power_off_seconds)
GPIO.output(pin, GPIO.LOW)

print("Complete")