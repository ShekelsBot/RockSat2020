#!/bin/bash
# VRSE Payload Software Auto Installation Script
#   Version 3.0
#
#  Contributors:
#    Andrew Bruckbauer
#    Konstantin Zaremski
#

# Display a nice banner
echo " "
echo "  // V.R.S.E (Virtual Reality Space Experience \\\\"
echo "    Auto Payload Computer Software Setup Script"

# Allow sudo usage without password
echo "    Allowing sudo usage without the password ('$USER ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers)"
sudo echo "$USER ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Set system hostname
echo "    Setting system hostname to VRSE"
sudo echo "VRSE" > /etc/hostname

# Update the system
echo "    Updating all mirrors and packages"
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "    Installing the necessary packages (git, vim, python3, python3-pip, i2c-tools, libusb-1.0-0-dev, build-essential, python-dev, python-pip, python-smbus)"
sudo apt install git vim python3 python3-pip i2c-tools libusb-1.0-0-dev build-essential python-dev python-pip python-smbus -y

# Install uhubctl
echo "    Installing uhubctl"
echo "  git clone https://github.com/mvp/uhubctl.git"
git clone https://github.com/mvp/uhubctl.git
echo "  cd uhubctl ; sudo make install ; cd ~"
cd uhubctl ; sudo make install ; cd ~

# Clone RockSat repository
echo "    Cloning the RockSat 2020 repository (git@github.com:ShekelsBot/RockSat2020.git)"
git clone git@github.com:ShekelsBot/RockSat2020.git

# Create output directories
echo "    Creating 'data', 'videos', and 'logs' directories"
mkdir -p ./RockSat2020/data
mkdir -p ./RockSat2020/videos
mkdir -p ./RockSat2020/logs

# Setting Python 3 to the default runtime
echo "    Setting Python v3.x to be the default Python runtime"
sudo update-alternatives --install /usr/bin/python python $(which python2) 1
sudo update-alternatives --install /usr/bin/python python $(which python3) 2

# Install Python packages with pip3
echo "    Installing Python packages with pip3 (RPI.GPIO, adafruit-blinka, adafruit-circuitpython-vl53l0x, adafruit-circuitpython-ADXL34x, adafruit-circuitpython-motorkit, picamera, psutil)"
pip3 install RPI.GPIO 
pip3 install adafruit-blinka
pip3 install adafruit-circuitpython-vl53l0x
pip3 install adafruit-circuitpython-ADXL34x
pip3 install adafruit-circuitpython-motorkit
pip3 install picamera
pip3 install psutil

# Install TMP006
echo "    Installing Adafruit Python TMP006"
git clone https://github.com/adafruit/Adafruit_Python_TMP.git
cd Adafruit_Python_TMP ; python setup.py install ; cd ~

# Enabling serial
#echo "    Enabling serial"
#sudo echo "" >> 

# Enabling I2C
echo "    Enabling i2c"
sudo echo "dtparam=i2c_arm=on" >> /boot/config.txt

# Enabling SPI
echo "    Enabling spi"
sudo echo "dtparam=spi=on" >> /boot/config.txt

# Enabling camera
echo "    Enabling camera"
sudo echo "start_x=1" >> /boot/config.txt
sudo echo "gpu_mem=128" >> /boot/config.txt
sudo echo "enable_uart=1" >> /boot/config.txt

# Disabling splash, delay, and BT
echo "    Disabling splash screen, boot delay, and bluetooth for a slightly faster boot time."
sudo echo "boot_delay=0" >> /boot/config.txt
sudo echo "disable_splash=1" >> /boot/config.txt
sudo echo "dtoverlay=pi3-disable-bt" >> /boot/config.txt

echo "INSTALLATION COMPLETE"
