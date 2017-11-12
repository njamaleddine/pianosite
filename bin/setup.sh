#!/bin/bash
# Production Setup for pianosite
# Assumes the OS is: Ubuntu 16.04
APP_NAME="pianosite"

# Update and install all packages
./bin/ubuntu/install_packages.sh

# install global python requirements
sudo pip install --upgrade pip
sudo pip install virtualenvwrapper

# Add virtualenvwrapper to path
cat ./bin/ubuntu/.bash_profile >> ~/.bash_profile
source `which virtualenvwrapper.sh`
# Setup virtual environment
mkvirtualenv --python=$(which python3) $APP_NAME
workon $APP_NAME

# download and setup solr
./bin/solr_setup.sh

# postgres setup (requires manual input)
export POSTGRES_PASSWORD=$(openssl rand -hex 64)
sudo -u postgres createuser --interactive
sudo -u postgres createdb $APP_NAME

# download and setup soundfont
mkdir ./tmp
wget https://github.com/musescore/MuseScore/raw/master/share/sound/FluidR3Mono_GM.sf3
mv ./tmp/FluidR3Mono_GM.sf3 apps/utility/fluidr3_gm2-2.sf2

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
