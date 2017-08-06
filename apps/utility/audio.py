# -*- coding: utf-8 -*-
import logging
import os
import subprocess

from django.conf import settings
from django.core.files import File
from pydub import AudioSegment


logger = logging.getLogger(__name__)


class MidiFile(File):
    """ A subclass of File for handling Midi Files """
    def __init__(self, file, soundfont_path=settings.MIDISHOP_SOUNDFONT_PATH):
        super(MidiFile, self).__init__(file)
        self.soundfont_path = soundfont_path

    def convert_to_audio(self, output_type='oga'):
        """
        Creates an audio file of a given output_type from a midi file

        Requires fluidsynth to create audio files from midi

        params:

            `output_type`: accepted file output types (wav, oga, ogg, etc.)

        returns:
            `output_file_path`: the absolute file path for the audio file
        """
        if not self.soundfont_path:
            raise Exception('Soundfont file is required to convert midi into audio')

        file_path, file_name = os.path.split(self.name)
        file_name = os.path.splitext(file_name)[0]

        output_filename = '{}.{}'.format(file_name, output_type)
        output_file_path = '{}/{}'.format(file_path, output_filename)

        completed_call = subprocess.run(
            [
                'fluidsynth', '-T', output_type, '-F', output_file_path,
                '-ni', self.soundfont_path, self.name
            ]
        )
        completed_call.check_returncode()

        return output_file_path


class AudioFile(File):
    """ A subclass of File for handling Audio Files (ogg, oga, mp3) """
    ALLOWED_TYPES = ('mp3', 'ogg', 'oga')

    def __init__(self, file):
        super(AudioFile, self).__init__(file)

    def slice(self, seconds):
        """
        Uses pydub to slice n seconds from the middle of the song

        Output ogg and mp3 file types
        """
        length = seconds * 1000
        song = None

        try:
            file_path, file_name = os.path.split(self.name)
            file_name, file_extension = os.path.splitext(file_name)
            file_extension = file_extension.replace('.', '')

            if file_extension == 'oga':
                file_extension = 'ogg'
                song = AudioSegment.from_ogg(self.name)
            elif file_extension == 'mp3':
                song = AudioSegment.from_mp3(self.name)

            if song:
                if song.duration_seconds * 1000 <= length:
                    # If the song is less than 30 seconds, give them half
                    song = song[:(song.duration_seconds / 2) * 1000]

                else:
                    lower_bound = length - (length / 2)
                    song = song[lower_bound:(length * 2) - lower_bound].fade_in(2000).fade_out(3000)

                slice_file_path = '{}/{}_slice.{}'.format(file_path, file_name, file_extension)
                song.export(slice_file_path, format=file_extension)

                return slice_file_path

        except IOError as e:
            logger.error(e, extra={'error_code': e.errno})

    def save_as_type(self, new_file_extension):
        """ Export audio given the new file extension """
        if new_file_extension not in self.ALLOWED_TYPES:
            raise Exception(
                'File extension must be: {}'.format(', '.join(self.ALLOWED_TYPES))
            )

        file_name, file_extension = os.path.splitext(self.name)
        file_extension = file_extension.replace('.', '')

        song = AudioSegment.from_file(self.name, format=file_extension)
        mp3_filename = '{}.{}'.format(file_name, new_file_extension)
        mp3_file = song.export(mp3_filename, format=new_file_extension)
        return mp3_file
