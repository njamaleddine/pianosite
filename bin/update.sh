#!/bin/bash
# Update application
# Assumes the OS is: Ubuntu 16.04
cd ~/pianosite
workon pianosite
git fetch origin
git merge origin/master

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic

# restart systemd application services
./bin/restart.sh
