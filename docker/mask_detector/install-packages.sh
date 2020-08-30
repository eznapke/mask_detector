#!/bin/bash

# Bash "strict mode", to help catch problems and bugs in the shell
# script. Every bash script you write should include this. See
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ for
# details.
set -euo pipefail

# Tell apt-get we're never going to be able to give manual
# feedback:
export DEBIAN_FRONTEND=noninteractive

# Update the package listing, so we know what package exist:
apt-get update

# Install security updates:
apt-get -y upgrade

# Install a new package, without unnecessary recommended packages:
#apt-get -y install --no-install-recommends python3-opencv
pip install opencv-python
pip install imutils
pip install tensorflow
pip install matplotlib

# apt-get -y install libgstreamer0.10-0-dbg libgstreamer0.10-0 libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev 
# apt-get -y install libunicap2 libunicap2-dev libdc1394-22-dev libdc1394-22 libdc1394-utils libv4l-0 libv4l-dev
# apt-get -y install libavcodec-dev libavformat-dev libswscale-dev
# apt-get -y install libdc1394-22-dev libdc1394-utils
# apt-get -y install libjpeg-dev libpng-dev libtiff-dev libjasper-dev
# apt-get -y install libtiff5 libtiff5-dev
# apt-get -y install libopenexr-dev
# apt-get -y install libjasper-dev

# Delete cached files we don't need anymore:
apt-get clean
rm -rf /var/lib/apt/lists/*
