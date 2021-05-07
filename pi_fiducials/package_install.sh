
#!/usr/bin/env bash
# Mostly adapted from this tutorial:
# https://www.pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/

# updates, dependencies, and optimizations
sudo apt-get update && sudo apt-get upgrade -y
# cmake for configuring opencv
sudo apt-get install -y build-essential cmake pkg-config
# allows us to load images, video streams
sudo apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng-dev
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install -y libxvidcore-dev libx264-dev
# GUI packages
sudo apt-get install -y libfontconfig1-dev libcairo2-dev
sudo apt-get install -y libgdk-pixbuf2.0-dev libpango1.0-dev
sudo apt-get install -y libgtk2.0-dev libgtk-3-dev
# optimizations
sudo apt-get install -y libatlas-base-dev gfortran
sudo apt-get install -y libhdf5-dev libhdf5-serial-dev libhdf5-103
sudo apt-get install -y libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
# python3 header files for compiling opencv
sudo apt-get install -y python3-dev

# install opencv and picamera with numpy dependencies
pip3 install --upgrade pip
pip3 install -U setuptools pip
pip3 install --upgrade pip setuptools wheel
pip3 install numpy
pip3 install imutils
pip3 install RPi.GPIO
pip3 install "picamera[array]"
pip3 install opencv-contrib-python==4.1.0.25
