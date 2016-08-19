# -*- coding: utf-8 -*-
""" Useful functions """
import uuid
from django.utils.crypto import get_random_string


def upload_file(self, file_name, random=False):
    """ Generate a Hashed Filepath for files """
    total_path_length = 0
    max_path_length = 98

    random_string = get_random_string(
        3, "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )
    uuid_string = uuid.uuid4().hex

    total_path_length = (
        len(random_string) +
        len(uuid_string) +
        len(file_name)
    )

    filename, file_extension = file_name.split('.')[0], file_name.split('.')[-1]
    file_name = '{}.{}'.format(filename, file_extension)

    # Crop the file name if it's too long
    if total_path_length > max_path_length:
        file_name = '{}.{}'.format(filename[0:25], file_extension)

    return '{}{}/{}'.format(
        random_string, uuid_string, file_name
    )


def get_file_name_from_path(path):
    try:
        filename = path.split("/")[-1]
    except:
        filename = path
    return filename


def get_file_name_without_extension(file_name):
    return file_name.split('.')[0]
