# coding=utf-8
"""
Signals related to catalogue
"""


def audio_slice_create(sender, instance, **kwargs):
    """ Create an audio slice from the MIDI File """
    instance.sample_audio = instance.process_file_data()
    instance.save()
