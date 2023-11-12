#!/bin/bash

echo "Installing the Dependencies"

#Ubuntu
yes|apt install wget curl zlib1g-dev libreadline-gplv2-dev libncurses5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev

#Debian Link
#https://linuxize.com/post/how-to-install-python-3-8-on-debian-10/

echo "Downloading Python3"
wget https://www.python.org/ftp/python/3.8.15/Python-3.8.15.tar.xz

echo "Extracting the zip"
tar -xvf Python-3.8.15.tar.xz
cd Python-3.8.15 && ./configure && make && make install

sleep 1m

echo "Getting PIP"
sleep 1m

wget https://bootstrap.pypa.io/get-pip.py
#Python-3.8.15/python get-pip.py
