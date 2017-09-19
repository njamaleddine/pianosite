#!/bin/bash
# Development Setup for pianosite
# Assumes the OS is: macOS Sierra
APP_NAME="pianosite"

brew install git
brew install python3
brew install postgres
brew install node
brew install fluid-synth --with-libsndfile
brew install ffmpeg
npm install -g less

# install global python requirements
sudo pip3 install --upgrade pip
sudo pip3 install virtualenvwrapper

# Activate Virtual Environment Requirements
# if virtualenvwrapper.sh is in your PATH (i.e. installed with pip)
source `which virtualenvwrapper.sh`
mkvirtualenv --python=$(which python3) $APP_NAME
workon $APP_NAME

# get and setup solr
./bin/solr-setup.sh

# download and setup soundfont
mkdir ./tmp && cd tmp/
wget http://www.musescore.org/download/fluid-soundfont.tar.gz
tar xopf fluid-soundfont.tar.gz
mv FluidR3\ GM2-2.SF2 ../apps/utility/fluidr3_gm2-2.sf2
cd ..

# create postgresql database
createdb $APP_NAME

# install all python packages
pip install -r requirements-dev.txt

# install node packages
npm install

# run db migrations
python manage.py migrate

# populate countries
python manage.py oscar_populate_countries

# replace the existing placeholder for media
cp static/oscar/img/placeholder.png > pianosite/public/media/

# copy over sample env file
cp sample.env > .env

# run the application
honcho start -f Procfile.dev
