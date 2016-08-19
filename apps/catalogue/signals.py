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
    audio_dict = instance.audio_conversion()
    sender.objects.filter(pk=instance.pk).update(
        full_audio=audio_dict['audio_url'],
        sample_ogg=audio_dict['ogg_audio_slice_url'],
        sample_mp3=audio_dict['mp3_audio_slice_url']
    )
