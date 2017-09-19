#!/bin/bash
# Production Setup for pianosite
# Assumes the OS is: Ubuntu 16.04
APP_NAME="pianosite"

# Update and install all packages
sudo apt-get update && apt-get upgrade && apt-get install -y \
 autoconf \
 build-essential \
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
 qt4-dev-tools

# install global python requirements
sudo pip3 install --upgrade pip
sudo pip3 install virtualenvwrapper

# Activate Virtual Environment Requirements
# if virtualenvwrapper.sh is in your PATH (i.e. installed with pip)
source `which virtualenvwrapper.sh`
mkvirtualenv --python=$(which python3) $APP_NAME
workon $APP_NAME

# download and setup solr
./bin/solr-setup.sh

# download and setup soundfont
mkdir ./tmp && cd tmp/
wget http://www.musescore.org/download/fluid-soundfont.tar.gz
tar xopf fluid-soundfont.tar.gz
cd ..
mv FluidR3\ GM2-2.SF2 apps/utility/fluidr3_gm2-2.sf2

# create the application db
createdb $APP_NAME

# install all production requirements
pip install -r requirements.txt

# install node packages
npm install

# run db migrations
python manage.py migrate

# populate countries
python manage.py oscar_populate_countries

# replace the existing placeholder for media
cp static/oscar/img/placeholder.png > pianosite/public/media/

# collect static files
python manage.py collectstatic

# copy over sample env file
cp sample.env > .env

# TODO: copy over nginx config
# TODO: setup upstart script
