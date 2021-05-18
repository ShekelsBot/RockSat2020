#Andrew Bruckbauer
#9/12/2020
#Raspberry PI Zero Camera Script
# Purpose of the sccript is to record and save the data to the pi

import picamera
import os
import psutil
import time

MAX_FILES = 1
DURATION = 20
SPACE_LIMIT = 80
TIME_STATUS_OK = 0.5

file_root = "/home/pi/videos/"

def pi_camera_test():

	if(psutil.disk_usage(".").percent > SPACE_LIMIT):
		print('WARNING: Low space!')
		exit()

	with picamera.PiCamera() as camera:
		camera.resolution = (1920,1080)
		camera.framerate = 30

		print('Searching files...')
		for i in range(1, MAX_FILES):
			file_number = i
			file_name = file_root + "test_video" + str(i).zfill(3) + ".h264"
			exists = os.path.isfile(file_name)
			if not exists:
				print ("Search Complete")
				break

		for file_name in camera.record_sequence(file_root + "video%03d.h264" % i for i in range(file_number, MAX_FILES)):
			timeout = time.time() + DURATION
			print('TEST Recording to %s' % file_name)

			while(time.time() < timeout):
				time.sleep(TIME_STATUS_OK)
				if(psutil.disk_usage(".").percent > SPACE_LIMIT):
					print('WARNING: Low space!')
					break;
