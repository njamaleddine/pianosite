# Pianosite Project Setup

An ecommerce web application for that sells MIDIs
**Pianosite** is an ecommerce web application built on top of [Oscar](https://github.com/django-oscar/django-oscar), a Django ecommerce platform.

Pianosite sells digital media in the form of MIDI files that other pianists/keyboard players can use to perform live at shows.
Samples of `.midi/.mid` files are in the form of `ogg` and `mp3`


##### Project Setup is only supported on Linux/OS X

### Project Dependencies
1. Install homebrew package manager. On Linux use the included package manager `apt`, etc. Homebrew should make it very simple for us to install most of the project dependencies.

2. Install [git](https://git-scm.com/)

        brew install git

3. Install [python3](https://www.python.org/)

        brew install python3

4. Install [PostgreSQL](http://www.postgresql.org/)

        brew install postgres

5. Install [Virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/index.html)

        sudo pip install virtualenvwrapper

    * Note: **Don't install any other dependencies using `sudo` after this. [Read more about virtual environments here](http://docs.python-guide.org/en/latest/dev/virtualenvs/)**

7. Install [node](https://nodejs.org/en/)
        brew install node

8. Install [sassc](https://github.com/sass/sassc)
        brew install sassc

### Project Setup
1. Create the database using the postgres cli:

        createdb pianosite

2. Clone repository:

        git clone git@bitbucket.org:njamaleddine/pianosite.git

3. Create a virtualenv:

        mkvirtualenv pianosite

4. Activate virtualenv:

        workon pianosite

5. Install requirements:

        pip install -r requirements.txt

6. Copy and Save `sample.env` as `.env` and update variables for local environment.

7. `pip install pycountry`

8. `python manage.py oscar_populate_countries`

9. Change default Site object domain to host domain instead of `example.com`

10. Copy `static/oscar/img/placeholder.png` to `pianosite/public/media/`

# Environment

Local environment run server:
        `honcho start -f Procfile.dev`

Production environment run server:
        `honcho start`

# Useful Commands
    python manage.py runserver_plus

    python manage.py shell_plus


# OS dependencies:

In order to get midi to audio conversion the environment needs to have:
* A Soundfont - http://musescore.org/en/handbook/soundfont (fluidr3_gm2-2.sf2)
* FluidSynth - `sudo apt-get install fluidsynth`
               `brew install fluid-synth --with-libsndfile`
* FFMPEG - `sudo apt-get install libav-tools`


# Test if Fluidsynth is working correctly with the soundfont
1. Enter this into the bash terminal:
        `fluidsynth -T oga -F gerudo_valley.mp3 -ni fluidr3_gm2-2.sf2 gerudo_valley.mid`

