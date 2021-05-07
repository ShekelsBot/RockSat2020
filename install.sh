#!/bin/bash
# VRSE Payload Software Auto Installation Script
#   Version 3.0

# Display a nice banner
echo " "
echo "  // V.R.S.E (Virtual Reality Space Experience \\\\"
echo "    Auto Payload Computer Software Setup Script"

# Allow sudo usage without password
echo "    Allowing sudo usage without the password\n('$USER ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers)"
sudo echo "$USER ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Update the system
echo "    Updating all mirrors and packages."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "    Installing the necessary packages (git, vim, python3, python3-pip, i2c-tools, libusb-1.0-0-dev)"
sudo apt install git vim python3 python3-pip i2c-tools libusb-1.0-0-dev -y

# Install uhubctl
echo "    Installing uhubctl."
echo "  git clone https://github.com/mvp/uhubctl"
git clone https://github.com/mvp/uhubctl
echo "  cd uhubctl ; sudo make install ; cd ~"
cd uhubctl ; sudo make install ; cd ~

# Create output directories
echo "    Create 'data', 'videos', and 'logs' directories."
mkdir -p data
mkdir -p videos
mkdir -p logs

# Setting Python 3 to the default runtime
echo "    Setting Python v3.x to be the default Python runtime."
sudo update-alternatives --install /usr/bin/python python $(which python2) 1
sudo update-alternatives --install /usr/bin/python python $(which python3) 2

# Install Python packages with pip3
echo "    Installing Python packages with pip3 (RPI.GPIO, adafruit-blinka)"
pip3 install RPI.GPIO 
pip3 install adafruit-blinka

# Old installer stuff VVV

## Install TMP006
#apt-get install build-essential python-dev python-pip python-smbus git
#pip install RPi.GPIO
#git clone https://github.com/adafruit/Adafruit_Python_TMP.git
#sleep 2
#cd Adafruit_Python_TMP
#python setup.py install
#cd /home/pi
## Install VL503L0X Library
#pip3 install adafruit-circuitpython-vl53l0x
## Install ADXL345
#pip3 install adafruit-circuitpython-ADXL34x
## Install motorkit
#pip3 install adafruit-circuitpython-motorkit
## Install picamera
#pip3 install picamera
## Install psutil
#pip3 install psutil
#cd ..
#mv RockSat2020_Bruckbauer/camera_scripts /home/pi/camera_scripts
#mv RockSat2020_Bruckbauer/control_2.py /home/pi/control_2.py
#mv RockSat2020_Bruckbauer/save_state.py /home/pi/save_state.py
#mv RockSat2020_Bruckbauer/save_creator.py /home/pi/save_creator.py
##load inital save_state to 0
#python save_creator.py
##remove save_creator
#rm -f save_creator.py
##give executable rights to camera scripts
#cd camera_scripts/
#chmod +x camera_control.sh
#chmod +x camera_control_off.sh
#chmod +x camera_control_on.sh
#echo "Installed"
#sleep 1
#echo "Remember to enable serial, i2c, spi, and pi-camera"
#echo "Run sudo raspi-config to enable these options"
