# Pianosite Project Setup

1. Clone repository
2. Create a virtualenv `mkvirtualenv pianosite`
3. Activate virtualenv `workon pianosite`
4. Install requirements `pip install -r requirements.txt`
5. Copy `sample.env` to `.env`


# Environment

Local environment run server:
    `foreman start -f Procfile.dev`

Production environment run server:
    `foreman start`


# About

**Pianosite** is an ecommerce site built on top of Oscar, a Django ecommerce platform.

Pianosite sells digital media in the form of .mid files that other pianists/keyboard players can use to perform live at shows.
Samples of `.midi/.mid` files are in the form of `ogg` and `mp3`


# OS dependencies:

In order to get midi to audio conversion the environment needs to have:
* A Soundfont - http://musescore.org/en/handbook/soundfont (fluidr3_gm2-2.sf2)
* FluidSynth - `sudo apt-get install fluidsynth`
* FFMPEG - `sudo apt-get install libav-tools`