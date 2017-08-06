# -*- coding: utf-8 -*-
# Catalogue models
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from oscar.apps.catalogue.abstract_models import AbstractProduct

from apps.utility.audio import AudioFile, MidiFile
from apps.utility.files import upload_file
from apps.utility.models import TimeStampedModel


class Artist(TimeStampedModel):
    name = models.CharField(max_length=255)

    class Meta (object):
        ordering = ('name',)

    def __str__(self):
        return '{0}'.format(self.name)


class Genre(TimeStampedModel):
    name = models.CharField(max_length=255)

    class Meta (object):
        ordering = ('name',)

    def __str__(self):
        return '{0}'.format(self.name)


class Product(AbstractProduct):
    artist = models.ForeignKey(Artist, null=True, blank=True)
    genre = models.ForeignKey(Genre, null=True, blank=True)
    midi_file = models.FileField(upload_to=upload_file, max_length=1024)
    full_audio = models.FileField(upload_to=upload_file, max_length=1024, blank=True, null=True)
    sample_ogg = models.FileField(upload_to=upload_file, max_length=1024, blank=True, null=True)
    sample_mp3 = models.FileField(upload_to=upload_file, max_length=1024, blank=True, null=True)

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)

        if self.midi_file:
            # Generate audio from midi and create sample audio in mp3 and ogg format
            # TODO: optimize to speed up save method, or throw into celery queue
            with open(self.midi_file.path, 'rb+') as midi_file:
                midi = MidiFile(midi_file)

                with open(midi.convert_to_audio(), 'rb+') as audio_file:
                    audio = AudioFile(audio_file)
                    sample_ogg = audio.slice(seconds=settings.MIDISHOP_AUDIO_SAMPLE_LENGTH)

                    with open(sample_ogg, 'rb+') as sample_ogg_file:
                        sample_ogg_audio = AudioFile(sample_ogg_file)
                        sample_mp3 = sample_ogg_audio.save_as_type('mp3')
                        sample_mp3_audio = AudioFile(sample_mp3)

                        self.full_audio.save(audio.name.split('/')[-1], audio, save=False)
                        self.sample_ogg.save(sample_ogg_audio.name.split('/')[-1], sample_ogg_audio, save=False)
                        self.sample_mp3.save(sample_mp3_audio.name.split('/')[-1], sample_mp3_audio, save=False)
        return super(Product, self).save(*args, **kwargs)


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
from oscar.apps.catalogue.models import *  # noqa
