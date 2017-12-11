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
source ~/.bash_profile

# Setup virtual environment
mkvirtualenv --python=$(which python3) $APP_NAME
workon $APP_NAME

# install all production requirements
pip install -r requirements.txt

# install node packages
npm install

# download and setup solr
./bin/solr_setup.sh

# postgres setup (requires manual input)
# export POSTGRES_PASSWORD=$(openssl rand -hex 64)
# sudo -u postgres createuser --interactive
# sudo -u postgres createdb $APP_NAME

# download and setup soundfont
mkdir ./tmp && cd ./tmp
wget https://s3.amazonaws.com/www.midisonline.com/fluidr3_gm2-2.sf2
cd ..
mv ./tmp/fluidr3_gm2-2.sf2 apps/utility/fluidr3_gm2-2.sf2

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

# Setup nginx config
sudo rm /etc/nginx/sites-enabled/default
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx_default.conf
sudo cp ./nginx.conf /etc/nginx/nginx.conf
sudo nginx -t
sudo touch /home/ubuntu/pianosite/access.log
sudo touch /home/ubuntu/pianosite/error.log
# use certbot (letsencrypt) to setup ssl cert
sudo certbot --nginx
sudo service nginx restart

# Setup ssl auto renewal
# This step is manual paste:  00 09 1 1 1 /home/ubuntu/pianosite/bin/ubuntu/renew_ssl.sh
sudo crontab -e

# copy over and start systemd script
./bin/update_services.sh

sudo systemctl enable pianosite_worker
sudo systemctl enable pianosite_scheduler
sudo systemctl enable pianosite_search
sudo systemctl enable pianosite_web

sudo systemctl start pianosite_worker
sudo systemctl start pianosite_scheduler
sudo systemctl start pianosite_search
sudo systemctl start pianosite_web
