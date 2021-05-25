#!/usr/bin/python
"""
    control - This is the main program for the VRSE payload.
    ** This script must be run with ~/RockSat2020 as the working directory
       with all of the directories (logs, data, video) and all of the files
       (config.ini) in place.
    Contributors:
        Andrew Bruckbauer
        Konstantin Zaremski
    Testing:
        The control program can be tested using the '--test' argument.
        Flat Sat (Default)      $ python control.py --test
        Flat Sat (Explicit)     $ python control.py --test flatsat
        Buttons                 $ python control.py --test buttons
        360_Camera              Just connect the inhibit wire
        ** During any test routine shutdown is simulated.
    Reset:
        The control program can be reset using the '--reset' argument.
        The reset argument clears any persisting save state so that operaiton
        can be tested as if running for the first time.
        $ python control.py --reset
        Flags can be supplied together (optional):    
        $ python control.py --reset --test
    Functionality:
        This program controls all VRSE functionality including arm extension
        and retraction, camera recording, and telemetry based on timer events
        provided by the host spacecraft.
    Spacecraft Battery Bus Timer Events:
        ID      Time    Description & Action
        GSE     T-30s   Spacecraft power is turned on and the Pi running this
                        control script boots up, loads this script as a service,
                        and waits unitl TE-R is triggered.
        TE-R    T+85s   The first timer event and one of two redundant lines is
                        powered, triggering motor extension and starting the 
                        video recording on the 360 degree camera.
        Interim         Between TE-R and TE-1 the camera will record the high
                        resolution 360 degree video at flight apogee.
        TE-1    T+261s  The first official timer event, but second for the VRSE
                        payload is powered triggering arm retraction and transfer
                        of the lower resolution file back to the Raspberry Pi for
                        data redundancy and durability if the camera is lost or
                        damaged during re-entry.
        TE-2    T+330s  The final timer event for the VRSE payload, which will
                        trigger a sync of filesystems and proper shutdown of the
                        Pi and other equipment for re-entry.
    Sensor Pins
        Temperature Sensor 1
            VCC - RED - 3.5v
            GND - BLK - Ground
            SDA - YLW - SDA
            SCL - BRN - SCL

        Accelerometer Sensor
            3v3 - RED - 3.5v
            GND - BLK - Ground
            SDA - YLW - SDA
            SCL - BRN - SCL

        Distance Sensor
            VIN - RED - 3.5v
            GND - BLK - Ground
            SDA - YLW - SDA
            SCL - BRN - SCL
"""

# Import dependencies
from multiprocessing import Process
import sys
import configparser
from RPi import GPIO
import datetime
from time import sleep, strftime
import board, busio, serial
import threading
import os
from adafruit_motorkit import MotorKit
import Adafruit_TMP.TMP006 as TMP006
import adafruit_vl53l0x
import adafruit_adxl34x

# Unique
from logger import Logger
import usbcamctl
import persist

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('./config.ini')

#Configure I2C 
i2c = busio.I2C(board.SCL, board.SDA)
 
# Configuration & setup tasks
TE_R = int(config['pinout']['TimerEventR'])                  # Spacecraft Battery Bus Timer Event (TE-R)
TE_1 = int(config['pinout']['TimerEvent1'])                  # Spacecraft Battery Bus Timer Event (TE-1)
TE_2 = int(config['pinout']['TimerEvent2'])                  # Spacecraft Battery Bus Timer Event (TE-2)
EXTEND_LIMIT = int(config['pinout']['ExtendLimitSwitch'])    # Arm Extension Limit Switch
RETRACT_LIMIT = int(config['pinout']['RetractLimitSwitch'])  # Arm Retraction Limit Switch
INHIBIT_1=int(config['pinout']['Inhibit_1'])                 # Flight Inhibit

# Whether or not timer events are triggered by an external signal (flatsat, mission) or 
EXTERNAL_TRIGGER = True

# Set GPIO mode
GPIO.setmode(GPIO.BCM)
# MotorKit class
kit = MotorKit(i2c=board.I2C())
arm = kit.motor3

# Setup GPIO
GPIO.setup(INHIBIT_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Shorthand
def armExtended(): return GPIO.input(EXTEND_LIMIT) == 0
def armRetracted(): return GPIO.input(RETRACT_LIMIT) == 0
def inhibit(id):
    if id == 1: return GPIO.input(INHIBIT_1) == 0
def TE(id):
    if id == "R": return (GPIO.input(TE_R) == 1 and EXTERNAL_TRIGGER) or (GPIO.input(TE_R) == 0 and not EXTERNAL_TRIGGER)
    if id == "1": return (GPIO.input(TE_1) == 1 and EXTERNAL_TRIGGER) or (GPIO.input(TE_1) == 0 and not EXTERNAL_TRIGGER)
    if id == "2": return (GPIO.input(TE_2) == 1 and EXTERNAL_TRIGGER) or (GPIO.input(TE_2) == 0 and not EXTERNAL_TRIGGER)

def TempConversion(c):
    return c * 9.0 / 5.0 + 32

# Start logging
Log = Logger()
Log.out("    V.R.S.E. Payload Control Program Started at system time: " + str(datetime.datetime.now().strftime("%Y-%m-%d T%H:%M:%S")) + ".")

def sensors():
    #    INIT SENSORS
    # Temperature Sensor 1
    sensor1 = TMP006.TMP006()
    sensor1 = TMP006.TMP006(address=0x40, busnum=1) # Default i2C address is 0x40 and bus is 1.
    sensor1.begin()
    # Accelerometer Sensor
    accelerometer = adafruit_adxl34x.ADXL345(i2c)
    # Distance Sensor
    vl53 = adafruit_vl53l0x.VL53L0X(i2c)

    # Start the sensor output file
    datafile = open("./data/vrse-sensors-" + str(datetime.datetime.now().strftime("%Y%m%d-T%H%M%S")) + ".csv", "w") 

    while True: 
        # Distance Sensor
        distance = vl53.range
        print ("Range: {0}mm".format(distance))
        #ser.write (b'Range: %d '%(distance)+b' mm \n')

        # Temperature Sensor 1
        obj1 = sensor1.readObjTempC()
        die1 = sensor1.readDieTempC()

        # Temperature Sensor 1 Serial out
        #ser.write (b'Sensor 1 object Temperature: %d \n'%(obj1))
        #ser.write (b'Sensor 1 die Temperature: %d \n'%(die1))
        print ('Object temperature: {0:0.3F}*C / {1:0.3F}*F'.format(obj1, TempConversion(obj1)))
        print ('Die temperature: {0:0.3F}*C / {1:0.3F}*F'.format(die1, TempConversion(die1)))
        sleep(.1)

        # Accelerometer tupple parse
        xAxis = (round(accelerometer.acceleration[0],1))
        yAxis = (round(accelerometer.acceleration[1],1))
        zAxis = (round(accelerometer.acceleration[2],1))

        
        # Accelerometer Serial out
        #ser.write (b'X Axis: %d \n'%(xAxis))
        #ser.write (b'Y Axis: %d \n'%(yAxis))
        #ser.write (b'Z Axis: %d \n'%(zAxis)) 
        print (f"Accelerometer (X:{xAxis},Y:{yAxis},Z:{zAxis})")
        
        # Output in CSV (Object Temperature, Die Temperature, Accel X, Accel Y, Accel Z, Distance)
        datafile.write(f"{str(obj1)},{str(die1)},{str(xAxis)},{str(yAxis)},{str(zAxis)},{str(distance)}")
        datafile.flush()
        sleep(0.5)

#Camera Testing before flight
def camera_testing():
    usbcamctl.usb(False) #USB Power off
    usbcamctl.power(True) #Power on
    usbcamctl.toggleRecord() #Toggle recording
    sleep(10)
    usbcamctl.toggleRecord() #Stop recording
    usbcamctl.usb(True) #Turn on power to USB

    Log_Test = Logger()
    # Mount and tranfer files
    if not os.path.isdir('/mnt/usb'): os.system("sudo mkdir -p /mnt/usb")
    if not os.path.isdir('video'): os.system("mkdir video")
    sleep(2)
    Log_Test.out("Mounting Camera")
    os.system("sudo mount -o ro /dev/sda1 /mnt/usb")
    sleep(4)
    Log_Test.out("Transfer footage")
    os.system("cp /mnt/usb/DCIM/*/*AB.MP4 ./video/")
    sleep(0.2)
    Log_Test.out("Syncing")
    os.system("sync")
    sleep(0.2)
    Log_Test.out("Unmounting camera")
    os.system("sudo umount /dev/sda1")
    sleep(1)
    #Power off camera
    Log_Test.out("Turning off camera")
    usbcamctl.power(False)

# Extend arm motor control operations
def extendArm():
    try:
        # If extend limit switch not hit, extend (positive throttle),
        # otherwise return True to signify extension
        if not armExtended():
            arm.throttle = 1
            sleep(1)
            while arm.throttle == 1:
                # Once extend limit is hit, set throttle to 0 and return True to signify extension
                if armExtended() or TE("1"):
                    arm.throttle = 0
                    return True
        else: return True
    except: return False

# Retract arm motor control operations
def retractArm():
    try:
        # If extend limit switch not hit, retract (negative throttle),
        # otherwise return True to signify retraction
        if not armRetracted():
            arm.throttle = -1
            sleep(1)
            while arm.throttle == -1:
                # Once retract limit is hit, set throttle to 0 and return True to signify retraction
                if armRetracted() or TE("2"):
                    arm.throttle = 0
                    return True
        else: return True
    except: return False

# Main program method
def main(arguments):
    if not os.path.isdir('data'): os.system("mkdir data")
    if not os.path.isdir('video'): os.system("mkdir video")
    if not os.path.isdir('logs'): os.system("mkdir logs")

    # Parse runtime arguments
    testing = False
    if ("--test" in arguments):
        testing = "flatsat"
        if (arguments.index("--test") != len(arguments) - 1) and arguments[arguments.index("--test") + 1] == "buttons":
            testing = "buttons"
    if ("--reset" in arguments): persist.clear()
    if ("--exit" in arguments): return True

    # If the inhibitor pin is set,
    if inhibit(1):
        persist.clear()
        camera_testing()
        sleep(2)
        if inhibit(1): os.system("sudo poweroff")
        return

    operating = True
   
    # Log opertation mode
    Log.out("    Operation Mode: " + "MISSION" if not testing else "TESTING")
    
    # Setup GPIO
    global EXTERNAL_TRIGGER
    if testing: EXTERNAL_TRIGGER = False if testing == "buttons" else True
    GPIO_TRIGGER_MODE = GPIO.PUD_DOWN if EXTERNAL_TRIGGER else GPIO.PUD_UP
    GPIO.setup(TE_R, GPIO.IN, pull_up_down=GPIO_TRIGGER_MODE)
    GPIO.setup(TE_1, GPIO.IN, pull_up_down=GPIO_TRIGGER_MODE)
    GPIO.setup(TE_2, GPIO.IN, pull_up_down=GPIO_TRIGGER_MODE)
    GPIO.setup(EXTEND_LIMIT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(RETRACT_LIMIT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    Log.out("GPIO Setup Complete.")

    # Disable motor throttle in case program crashed and was enabled
    arm.throttle = 0
    sleep(1)
    
    # Load previous state
    currentState = persist.read()
    if currentState: Log.out(f"Persisting state detected ({currentState}). Possible power failure has occurred.")
    else: Log.out("No persisting state was detected, proceeding with normal execution order.")

    # Identify power failures
    powerfailed = True if currentState != None else False

    # Begin recording sensor data (telemetry)
    if operating:
        #Log.out("Beginning sensor data collection and telemetry.")
        Log.out("Now listening to timer event signals.")
    # Main loop listening for timer events
    while operating:
        if TE("R") and (not currentState or currentState == "TE-R"):
            currentState = "TE-R"
            persist.set(currentState)
            Log.out("TE-R signal detected, beginning arm extension and video recording.")
            
            # Set up camera for recording 
            def record(alreadypower):
                recording = False
                usbOff = usbcamctl.usb(False)
                if usbOff:
                    Log.out("  USB ports have been disabled.")
                    camPower = usbcamctl.power(True) if not alreadypower else True
                    if camPower:
                        Log.out("  Camera has been sent the power on signal via. GPIO." if not alreadypower else "  Camera should already be powered on before the recorded power failure.")
                        recording = usbcamctl.toggleRecord()
                        if recording: Log.out("  Camera recording has been triggered via. GPIO.")
                        else: Log.out("  Failed to trigger camera recording.")
                    else: Log.out("  Failed to send camera power signal.")
                else: Log.out("  Failed to disable USB ports.")
                return recording

            # Asynchronous tasks via. multithreading
            status = {
                "recording": False,
                "extended": False
            }
            # Wrapper functions for multi threading
            def doRecord():
                status["recording"] = record(powerfailed)
                Log.out(f"The 360 degree camera is {'recording' if status['recording'] else 'not recording'}.")
                return
            def doExtend():
                status["extended"] = extendArm()
                Log.out(f"The arm is {'extended' if status['extended'] else 'not extended'}.")
                return
            # Create threads
            recordThread = threading.Thread(target=doRecord)
            recordThread.start()
            extendThread = threading.Thread(target=doExtend)
            extendThread.start()
            # Finish threads
            recordThread.join()
            extendThread.join()
            
            # Move on to the next 
            currentState = "TE-1"
            persist.set(currentState)
            Log.out("TE-R tasks are complete, waiting for TE-1 signal.")
        elif TE("1") and currentState == "TE-1":
            Log.out("TE-1 signal detected, retracting arm and transferring low quality footage to Pi.")

            # Retract Arm
            retraction = retractArm()
            Log.out(f"The arm is {'retracted' if retraction else 'not retracted'}.")

            # Stop recording and enable USB interface
            stoppedRecording = usbcamctl.toggleRecord()
            Log.out(f"The 360 degree camera is {'no longer recording' if stoppedRecording else 'still recording'}.")
            usbOn = usbcamctl.usb(True)
            Log.out(f"USB ports are {'now enabled' if usbOn else 'still disabled'}.")

            # Mount and tranfer files
            if not os.path.isdir('/mnt/usb'): os.system("sudo mkdir -p /mnt/usb")
            if not os.path.isdir('video'): os.system("mkdir video")
            sleep(2)
            Log.out("Mounting 360 degree camera SD card over USB.")
            os.system("sudo mount -o ro /dev/sda1 /mnt/usb")
            sleep(4)
            os.system("cp /mnt/usb/DCIM/*/*AB.MP4 ./video/")
            Log.out("All low resolution video files have been copied.")
            sleep(0.2)
            os.system("sync")
            Log.out("All buffers have been synchronized with their respective block devices.")
            sleep(0.2)
            Log.out("Unmounting 360 degree camera.")
            os.system("sudo umount /dev/sda1")
            sleep(1)

            # Power off the camera
            camOff = usbcamctl.power(False)
            Log.out(f"The camera is {'shut down' if camOff else 'still running'}.")

            # Move on to the next
            currentState = "TE-2"
            persist.set(currentState)
            Log.out("TE-1 tasks are completed, waiting for TE-2 signal.")
        elif TE("2") and currentState == "TE-2":
            Log.out("TE-2 signal detected, exiting signal listen mode and shutting down electronic systems.")
            currentState = "SPLASH"
            persist.set(currentState)
            operating = False
        elif currentState == "SPLASH":
            Log.out("SPLASH state, exiting signal listen mode and shutting down electronic systems.")
            operating = False
    
    # Sync to the drives & poweroff
    os.system("sync")
    
    # End logging
    Log.close()
    
    if not testing:
        sleep(1)
        os.system("sudo poweroff")

# Entry point
if __name__ == "__main__":
    try:
        arguments = sys.argv
        arguments.pop(0)

        p1 = Process(target=sensors)
        p1.start()
        p2 = Process(target=main(arguments))
        p2.start()

    except KeyboardInterrupt:
        print ("Caught KeyboardInterrupt exiting")
        p1.terminate()
        p2.terminate()

        p1.join()
        p2.join() 
