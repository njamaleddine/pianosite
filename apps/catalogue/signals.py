# coding=utf-8
"""
Signals related to catalogue
"""


def audio_creation(sender, instance, **kwargs):
    """ Create an audio slice from the MIDI File """
    output_filename, slice_file_name = instance.audio_conversion()
    sender.objects.filter(pk=instance.pk).update(full_audio=output_filename, sample_audio=slice_file_name)
