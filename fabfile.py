import re
import os
from fabric.api import local


def freeze():
    """ Overwrites requirements.txt. with the current pip dependencies """
    local("pip freeze > requirements.txt")


def read_env():
    try:
        with open('.env') as f:
            content = f.read()
    except IOError:
        content = ''

    for line in content.splitlines():
        m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
        if m1:
            key, val = m1.group(1), m1.group(2)
            m2 = re.match(r"\A'(.*)'\Z", val)
            if m2:
                val = m2.group(1)
            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r'\\(.)', r'\1', m3.group(1))
            os.environ.setdefault(key, val)


def run(*args, **kwargs):
    """ Runs a command with the environment variables loaded """
    read_env()
    local(*args)


def manage(cmd, prefix="python"):
    """ Loads the environment before running the manage command. """
    run("{0} manage.py {1}".format(prefix, cmd))


def shell():
    """ Opens a shell running ipython """
    manage("shell -i ipython")
