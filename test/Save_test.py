# Andrew Bruckbauer
# 
from time import sleep
import RPi.GPIO as GPIO
import board
import subprocess
import pickle
from adafruit_motorkit import MotorKit
GPIO.setmode(GPIO.BCM)

filename = 'save_state'
infile = open(filename, 'rb')
new_save = pickle.load(infile)
infile.close()
current_state = new_save

kit = MotorKit(i2c=board.I2C())
button1=18
#Event 1
button2=27
#Event 2
button3=22
#Event 3
limit_1=23
#Arm closed switch
limit_2=24
#Arm open switch

GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(limit_1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(limit_2,GPIO.IN,pull_up_down=GPIO.PUD_UP)

print ("Program Started press buttons to simulate events")
print ("Save State Test ")
print ("Current Save State is: "+str(new_save))

while (1):
    #First Condtion loop with single fail state
    if GPIO.input(button1)==0 or new_save==1:
        if current_state == 0:
            current_state == 1
            print ('Updated Save state is now: '+current_state)
            outfile = open (filename,'wb')
            pickle.dump(current_state,outfile)
            outfile.close()

            print ("Button 1 Pressed")
            print ("Arm Extension")
            sleep (.1)
        elif GPIO.input(limit_2)==1:

            current_state == 2
            print ('Updated Save state is now: '+current_state)
            outfile = open (filename,'wb')
            pickle.dump(current_state,outfile)
            outfile.close()

            kit.motor3.throttle = 1
            sleep (1)
            while kit.motor3.throttle == 1:
                if GPIO.input(limit_2)==0:

                    current_state == 3
                    print ('Updated Save state is now: '+current_state)
                    outfile = open (filename,'wb')
                    pickle.dump(current_state,outfile)
                    outfile.close()

                    kit.motor3.throttle = 0
                    print ("Starting Camera Script RECORD")
                    sleep (.5)
                    subprocess.call("./camera_scripts/camera_control_on.sh", shell=True)
                    #call other script
                elif kit.motor3.throttle == 0:
                    current_state == 4
                    print ('Updated Save state is now: '+current_state)
                    outfile = open (filename,'wb')
                    pickle.dump(current_state,outfile)
                    outfile.close()
                    break
    #Second State single save condition
    if  GPIO.input(button2)==0 or current_state==5:
        if current_state == 4:
            current_state == 5
            print ('Updated Save state is now: '+current_state)
            outfile = open (filename,'wb')
            pickle.dump(current_state,outfile)
            outfile.close()

            print ("Button 2 Pressed")
            print ("Arm Retraction")
        elif GPIO.input(limit_1)==1:

            current_state == 6
            print ('Updated Save state is now: '+current_state)
            outfile = open (filename,'wb')
            pickle.dump(current_state,outfile)
            outfile.close()

            kit.motor3.throttle = -1
            sleep(.5)
            print ("Camera data script TRANSFER")
            while kit.motor3.throttle == -1:
                if GPIO.input(limit_1)==0:

                    current_state == 7
                    print ('Updated Save state is now: '+current_state)
                    outfile = open (filename,'wb')
                    pickle.dump(current_state,outfile)
                    outfile.close()

                    kit.motor3.throttle = 0
                    print ("arm closed")
                    print ("starting camera scripts")
                    subprocess.call("./camera_scripts/camera_control_off.sh", shell=True)
                elif kit.motor3.throttle == 0:

                    current_state == 8
                    print ('Updated Save state is now: '+current_state)
                    outfile = open (filename,'wb')
                    pickle.dump(current_state,outfile)
                    outfile.close()

                    break
    #Third Contion save state w/ file reset
    if  GPIO.input(button3)==0 or new_save==9:

        current_state == 9
        print ('Updated Save state is now: '+current_state)
        outfile = open (filename,'wb')
        pickle.dump(current_state,outfile)
        outfile.close()

        print ("Button 3 Pressed")
        print ("simulation shutdown event")
        kit.motor3.throttle = 0
        #RESET SAVE FILE
        current_state == 0
        print ('Updated Save state is now: '+current_state)
        outfile = open (filename,'wb')
        pickle.dump(current_state,outfile)
        outfile.close()
        #Turn off raspberry pi
        sleep(.5)
        break