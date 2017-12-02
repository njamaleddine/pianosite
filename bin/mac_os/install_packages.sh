#!/bin/bash
# Development Setup for pianosite
# Assumes the OS is Mac OS

# Update and install all packages
echo "Updating and installing brew packages for mac os..."
brew update && brew upgrade

brew install git
brew install python3
brew install postgres
brew install node
brew install fluid-synth --with-libsndfile
brew install ffmpeg
brew install libmagic

brew cleanup

npm install -g less
