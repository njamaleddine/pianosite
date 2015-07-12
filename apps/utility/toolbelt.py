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


def coerce_int(value):
    """ Coerce integer value """
    if value:
        if isinstance(value, int):
            return value
        else:
            try:
                value = int(value)
            except (TypeError, ValueError):
                return -1
    return False


def coerce_bool(value):
    """ Coerce boolean value """
    if value:
        if isinstance(value, bool):
            return value
        elif str(value).lower() == 'true' or str(value) == str(1):
            return True
    return False


def upload_to_s3(self, file_name, sub_directory=""):
    """ Generate a Hashed Filepath for files """
    total_path_length = 0
    max_path_length = 98

    random_string = get_random_string(3, "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    date_hash = generate_date_hash()

    total_path_length = len(sub_directory) + len(random_string) + len(date_hash) + len(file_name)

    # create a series of directories
    # to limit the number of files in any given directory
    name_dir_path = file_extension = '/'.join(
        file_name[:-1 * (len(file_name.split(".")[-1]) + 1)][:10].lower()
    )

    # Crop the file name if it's too long
    if total_path_length > max_path_length:
        file_extension = file_name.split(".")[-1]
        file_name = file_name[0:35] + "." + file_extension

    return u'{0}/{1}/{2}{3}/{4}'.format(sub_directory, name_dir_path, random_string, date_hash, file_name)


def strip_non_alphanumeric(string):
    """ Strip non alphanumeric characters """
    non_alpha_numeric = re.compile(r'[^0-9a-zA-Z]+')

    return non_alpha_numeric.sub('', string)


def standardize_phone_number(phone_number):
    new_phone_number = ""

    if phone_number:
        phone_number = strip_non_alphanumeric(phone_number)
        phone_number = re.compile(r'[^0-9]+').sub('x', phone_number)

        split_phone_extension = phone_number.split('x')

        phone_number = split_phone_extension[0]
        new_phone_number = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1-", "%d" % int(phone_number[:-1])) + phone_number[-1]

        if len(split_phone_extension) > 1:
            extension = split_phone_extension[1]
            new_phone_number = u"{0}x{1}".format(new_phone_number, extension)

    return new_phone_number
