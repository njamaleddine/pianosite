""" Useful functions """

import re
import hashlib
from datetime import datetime
from django.utils.crypto import get_random_string

from django.conf import settings


def generate_date_hash():
    """
    Generate a hashed date of the current time
    """
    hasher = hashlib.sha256()
    hasher.update(str(datetime.now()))
    hashed_date = hasher.hexdigest()[0:30]

    return hashed_date


def upload_file(self, file_name, random=False):
    """ Generate a Hashed Filepath for files """
    total_path_length = 0
    max_path_length = 98

    random_string = get_random_string(
        3, "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )
    date_hash = generate_date_hash()

    total_path_length = (
        len(settings.MEDIA_ROOT) +
        len(random_string) +
        len(date_hash) +
        len(file_name)
    )

    # Crop the file name if it's too long
    if total_path_length > max_path_length:
        file_extension = file_name.split(".")[-1]
        file_name = file_name[0:35] + "." + file_extension

    return u'{0}/{1}{2}/{3}'.format(
        settings.MEDIA_ROOT, random_string, date_hash, file_name
    )


def strip_non_alphanumeric(string):
    """ Strip non alphanumeric characters """
    non_alpha_numeric = re.compile(r'[^0-9a-zA-Z]+')

    return non_alpha_numeric.sub('', string)
