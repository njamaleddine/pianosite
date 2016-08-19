#!/bin/bash
brew install git
brew install python3
brew install postgres
brew install node
brew install sassc
brew install fluid-synth --with-libsndfile
brew install ffmpeg
sudo pip install virtualenvwrapper

createdb pianosite

git clone git@bitbucket.org:njamaleddine/pianosite.git

mkvirtualenv pianosite --python=($which python3)

pip install -r requirements.txt

python manage.py oscar_populate_countries

cp static/oscar/img/placeholder.png > pianosite/public/media/