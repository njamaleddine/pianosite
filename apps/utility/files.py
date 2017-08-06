# -*- coding: utf-8 -*-
import uuid


def upload_file(self, file_name, random=False):
    """ Generate a unique filepath for files """
    total_path_length = 0
    max_path_length = 98

    uuid_string = uuid.uuid4().hex

    total_path_length = len(uuid_string) + len(file_name)

    filename, file_extension = file_name.split('.')[0], file_name.split('.')[-1]
    file_name = '{}.{}'.format(filename, file_extension)

    # Crop the file name if it's too long
    if total_path_length > max_path_length:
        file_name = '{}.{}'.format(filename[0:25], file_extension)

    return '{}/{}'.format(uuid_string, file_name)
