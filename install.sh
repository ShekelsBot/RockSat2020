#!/bin/bash
# Installer 2.0
cd /home/pi
mkdir videos
mkdir data
mkdir /mnt/usb-drive
apt-get update
apt-get upgrade -y
apt-get install python3-pip
pip3 install --upgrade setuptools
apt-get install -y python3 git python3-pip
#Set Python 3 to default
sudo update-alternatives --install /usr/bin/python python $(which python2) 1
sudo update-alternatives --install /usr/bin/python python $(which python3) 2
#i2c Tools
apt-get install python3-dev python3-pip python3-smbus i2c-tools -y
apt-get install libusb-1.0-0-dev -y
# update-alternatives --config python
pip3 install RPI.GPIO 
pip3 install adafruit-blinka
# Install TMP006
apt-get install build-essential python-dev python-pip python-smbus git
pip install RPi.GPIO
git clone https://github.com/adafruit/Adafruit_Python_TMP.git
sleep 2
cd Adafruit_Python_TMP
python setup.py install
cd /home/pi
# Install VL503L0X Library
pip3 install adafruit-circuitpython-vl53l0x
# Install ADXL345
pip3 install adafruit-circuitpython-ADXL34x
# Install motorkit
pip3 install adafruit-circuitpython-motorkit
# Install picamera
pip3 install picamera
# Install psutil
pip3 install psutil
# Install uhubctl
git clone https://github.com/mvp/uhubctl
sleep 2
cd uhubctl
make
make install
echo "Installed"
sleep 1
echo "Remember to enable serial, i2c, spi, and pi-camera"
echo "Run sudo raspi-config to enable these options"
