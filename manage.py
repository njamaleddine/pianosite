#!/usr/bin/env python
import os
import sys

from django.core.management import execute_from_command_line
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pianosite.settings")

    execute_from_command_line(sys.argv)
