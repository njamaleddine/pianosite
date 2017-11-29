#!/bin/bash
# Production Setup for pianosite
# Assumes the OS is Ubuntu 16.04

# Update and install all packages
echo "Updating and installing all Ubuntu packages"
sudo apt-get update -y && apt-get upgrade -y && apt-get install -y \
 autoconf \
 build-essential \
 default-jre \
 ffmpeg \
 fluidsynth \
 git \
 idle-python2.7 \
 lib32ncurses5-dev \
 libav-tools \
 libffi-dev \
 libgle3 \
 libicu-dev \
 libjpeg8-dev \
 libldap2-dev \
 libmagic1 \
 libpq-dev \
 libqt4-dbus \
 libqt4-network \
 libqt4-script \
 libqt4-test \
 libqt4-xml \
 libqtcore4 \
 libqtgui4 \
 libsasl2-dev \
 libtool \
 libxml2-dev \
 libxslt1-dev \
 nginx \
 nodejs \
 npm \
 pkg-config \
 postgresql \
 postgresql-contrib \
 python-dev \
 python-imaging \
 python-numpy \
 python-opengl \
 python-pyrex \
 python-pyside.qtopengl \
 python-qt4 \
 python-qt4-gl \
 python-setuptools \
 python3-dev \
 python3-pip \
 qt4-designer \
 qt4-dev-tools \
 redis-server \


# install certbot for letsencrypt.org
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install python-certbot-nginx
