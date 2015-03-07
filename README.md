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