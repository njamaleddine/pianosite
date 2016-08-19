# -*- coding: utf-8 -*-
"""
Signals related to catalogue
"""
from __future__ import unicode_literals, absolute_import


def audio_creation(sender, instance, **kwargs):
    """
    Create an audio slice from the MIDI File

    TODO:
    Only update generate the audio if this is the first time or the midi
    was changed.
    """
    output_filename, slice_file_name = instance.audio_conversion()
    sender.objects.filter(pk=instance.pk).update(
        full_audio=output_filename, sample_audio=slice_file_name
    )
