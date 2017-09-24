#!/bin/bash
# Production Setup for pianosite
# Assumes the OS is: Ubuntu 16.04
APP_NAME="pianosite"

# Update and install all packages
sudo apt-get update && apt-get upgrade && apt-get install -y \
 autoconf \
 build-essential \
 default-jre \
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
 redis-server

# install global python requirements
sudo pip3 install --upgrade pip
sudo pip3 install virtualenvwrapper

# Activate Virtual Environment Requirements
# if virtualenvwrapper.sh is in your PATH (i.e. installed with pip)
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source `which virtualenvwrapper.sh`
mkvirtualenv --python=$(which python3) $APP_NAME
workon $APP_NAME

# download and setup solr
./bin/solr_setup.sh

# postgres setup (requires manual input)
export POSTGRES_PASSWORD=$(openssl rand -hex 64)
sudo -u postgres createuser --interactive
sudo -u postgres createdb $APP_NAME

# download and setup soundfont
mkdir ./tmp && cd tmp/
wget https://github.com/musescore/MuseScore/raw/master/share/sound/FluidR3Mono_GM.sf3
mv FluidR3Mono_GM.sf3 apps/utility/fluidr3_gm2-2.sf2
cd ..

# install all production requirements
pip install -r requirements.txt

# install node packages
npm install

# setup .env file
# note, you'll still need to populate some of these variables (see blank ones)
./bin/setup_env.sh

# run db migrations
python manage.py migrate

# populate countries
python manage.py oscar_populate_countries

# setup default store data
python manage.py setup_store

# replace the existing placeholder for media
cp static/oscar/img/placeholder.png pianosite/public/media/placeholder.png

# collect static files
python manage.py collectstatic

# copy nginx config
sudo mkdir /etc/nginx/sites-available/$APP_NAME
sudo cp ./nginx.conf /etc/nginx/sites-available/pianosite
sudo ln -s /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/
sudo nginx -t
sudo service nginx restart

# TODO: setup upstart script
