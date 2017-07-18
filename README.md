# Pianosite Project Setup

An ecommerce web application for that sells MIDIs
**Pianosite** is an ecommerce web application built on top of [Oscar](https://github.com/django-oscar/django-oscar), a Django ecommerce platform.

Pianosite sells digital media in the form of MIDI files that other pianists/keyboard players can use to perform live at shows.
Samples of `.midi/.mid` files are in the form of `ogg` and `mp3`

> **Note:** Project Setup is only supported on macOS


## Project Setup (development)

1. Install the [homebrew](https://brew.sh/) package manager

2. Run the project setup:
```
bin/dev-setup.sh
```

* Dependencies installed in the project setup: 
   * [`git`](https://git-scm.com/)
   * [`python3`](https://www.python.org/)
   * [`PostgreSQL`](http://www.postgresql.org/)
   * [`Virtualenvwrapper`](https://virtualenvwrapper.readthedocs.org/en/latest/index.html)
   * [`node`](https://nodejs.org/en/)
   * [`lessc`](https://nodejs.org/en/)
   * [`ffmpeg`](https://ffmpeg.org/)
   * [`FluidSynth`](http://www.fluidsynth.org/)
   * [`A Soundfont (fluidr3_gm2-2.sf2)`](http://www.musescore.org)  

 * In order to get midi to audio conversion the environment needs to have: `ffmpeg`, `FluidSynth`, `A Soundfont`

3. Change default [Site](https://docs.djangoproject.com/en/dev/ref/contrib/sites/) object domain to host domain instead of `example.com`

4. For production setup run `./bin/setup.sh`

## Environment

Local environment run server:
    
    honcho start -f Procfile.dev

Production environment run server:
    
    honcho start

## Useful Commands
    ./bin/less.sh - compile less to css

    python manage.py shell_plus - open up interactive python shell

## Test if Fluidsynth is working correctly with the soundfont
1. Enter this into the bash terminal:
        `fluidsynth -T oga -F gerudo_valley.mp3 -ni fluidr3_gm2-2.sf2 gerudo_valley.mid`

