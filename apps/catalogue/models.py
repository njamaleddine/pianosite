# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

# Catalogue models
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from oscar.apps.catalogue.abstract_models import AbstractProduct

from apps.utility.models import TimeStampedModel
from apps.utility.toolbelt import upload_file, get_file_name_from_path
from apps.utility.process_midi import convert_to_audio, slice_audio, ogg_to_mp3

from pianosite.settings import BASE_DIR


@python_2_unicode_compatible
class Artist (models.Model):
    name = models.CharField(max_length=255)

    class Meta (object):
        ordering = ('name',)

    def __str__(self):
        return '{0}'.format(self.name)


@python_2_unicode_compatible
class Genre (models.Model):
    name = models.CharField(max_length=255)

    class Meta (object):
        ordering = ('name',)

    def __str__(self):
        return '{0}'.format(self.name)


class Product (AbstractProduct):
    artist = models.ForeignKey(Artist, null=True, blank=True)
    genre = models.ForeignKey(Genre, null=True, blank=True)
    midi_file = models.FileField(upload_to=upload_file, max_length=1024)
    full_audio = models.FileField(upload_to=upload_file, max_length=1024, blank=True, null=True)
    sample_ogg = models.FileField(upload_to=upload_file, max_length=1024, blank=True, null=True)
    sample_mp3 = models.FileField(upload_to=upload_file, max_length=1024, blank=True, null=True)

    def audio_conversion(self):
        """
        Generate audio from midi and create sample audio in mp3 and ogg format

        TODO: optimize to speed up save method, or throw into celery queue
        """
        if self.midi_file:
            midi_file_name = self.midi_file.path.split('/')[-1]
            audio_directory = self.midi_file.path.replace(midi_file_name, '')
            audio_base_url = self.midi_file.url.replace(midi_file_name, '')

            audio_path, audio_filename, = convert_to_audio(
                midi_filename=self.midi_file.path,
                soundfont='{}/{}'.format(BASE_DIR, 'apps/utility/fluidr3_gm2-2.sf2'),
                output_path='{}'.format(audio_directory),
                output_types=['oga']
            )
            slice_file_name = slice_audio(audio_file_name=audio_path)

            # convert slice to mp3 to support safari
            # convert ogg to mp3 (sometimes fluidsynth doesn't do midi -> mp3)
            sample_mp3 = ogg_to_mp3(slice_file_name)

            audio_url = '{}{}'.format(audio_base_url, audio_filename)
            ogg_audio_slice_url = '{}{}'.format(
                audio_base_url, get_file_name_from_path(slice_file_name)
            )
            mp3_audio_slice_url = '{}{}'.format(audio_base_url, get_file_name_from_path(sample_mp3))

            return {
                'audio_url': audio_url,
                'ogg_audio_slice_url': ogg_audio_slice_url,
                'mp3_audio_slice_url': mp3_audio_slice_url
            }
        else:
            raise 'No midi file available with this object'

    def save(self, *args, **kwargs):
        audio_dict = self.audio_conversion()
        self.full_audio = audio_dict['audio_url']
        self.sample_ogg = audio_dict['ogg_audio_slice_url']
        self.sample_mp3 = audio_dict['mp3_audio_slice_url']
        return super(Product, self).save(*args, **kwargs)


@python_2_unicode_compatible
class MidiDownloadURL(TimeStampedModel):
    """ The midi download url available for the user to access the file """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product)
    owner = models.ForeignKey(User, blank=True, null=True)
    customer_email = models.EmailField(blank=True)
    date_redeemed = models.DateTimeField(blank=True, null=True)
    downloads_left = models.IntegerField(default=2)

    def __str__(self):
        return '{}'.format(self.uuid)

    @property
    def expired(self):
        if self.date_redeemed and self.downloads_left < 1:
            return True
        return False

    @property
    def file(self):
        if not self.expired:
            return self.product.midi_file
        return None

    @property
    def file_name(self):
        return self.file.path.split('/')[-1]


# Required to import the rest of the oscar models unfortunately
from oscar.apps.catalogue.models import *
