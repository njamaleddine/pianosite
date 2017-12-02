# -*- coding: utf-8 -*-
# Catalogue models
import uuid

import magic
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from oscar.apps.catalogue.abstract_models import AbstractProduct

from apps.utility.audio import AudioFile, MidiFile
from apps.utility.files import upload_file
from apps.utility.models import TimeStampedModel
from .tasks import update_search_index


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
    """
    Midishop Product class that handles both midi files and pdf sheet music
    """
    artist = models.ForeignKey(Artist, null=True, blank=True)
    genre = models.ForeignKey(Genre, null=True, blank=True)
    upload = models.FileField(upload_to=upload_file, max_length=1024)
    full_audio = models.FileField(upload_to=upload_file, max_length=1024, blank=True, null=True)
    sample_ogg = models.FileField(upload_to=upload_file, max_length=1024, blank=True, null=True)
    sample_mp3 = models.FileField(upload_to=upload_file, max_length=1024, blank=True, null=True)

    @property
    def mime_type(self):
        if self.upload._file:
            return magic.from_buffer(self.upload._file.read(1024), mime=True)
        with open(self.upload.path, mode='rb') as product_file:
            return magic.from_buffer(product_file.read(1024), mime=True)
        return None

    def reset_fields(self):
        """
        Clear out audio fields so that changes in mime_type don't leave audio
        samples (ex. changing type)
        """
        self.full_audio = None
        self.sample_ogg = None
        self.sample_mp3 = None

    def clean(self, *args, **kwargs):
        self.reset_fields()
        cleaned_data = super().clean(*args, **kwargs)

        if self.product_class.name.lower() == 'midi' and self.mime_type != 'audio/midi':
            raise ValidationError(
                _(
                    'You must upload a midi for a midi product, change '
                    'the product type or upload a midi to continue'
                )
            )
        return cleaned_data

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)

        if self.upload and self.mime_type == 'audio/midi':
            # Generate audio from midi and create sample audio in mp3 and ogg format
            # TODO: optimize to speed up save method, or throw into celery queue
            with open(self.upload.path, 'rb+') as upload:
                midi = MidiFile(upload)

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
    """
    A download url available for the user to access the product upload file

    This may be either a midi or a sheet music file (like a pdf)
    """
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
            return self.product.upload
        return None

    @property
    def file_name(self):
        return self.file.path.split('/')[-1]


# Required to import the rest of the oscar models unfortunately
from oscar.apps.catalogue.models import *  # noqa


@receiver(models.signals.post_save, sender=Artist)
@receiver(models.signals.post_save, sender=Genre)
@receiver(models.signals.post_save, sender=Product)
@receiver(models.signals.post_save, sender=Category)
@receiver(models.signals.post_save, sender=ProductClass)
@receiver(models.signals.post_save, sender=ProductCategory)
@receiver(models.signals.post_delete, sender=Artist)
@receiver(models.signals.post_delete, sender=Genre)
@receiver(models.signals.post_delete, sender=Product)
@receiver(models.signals.post_delete, sender=Category)
@receiver(models.signals.post_delete, sender=ProductClass)
@receiver(models.signals.post_delete, sender=ProductCategory)
def update_search_index_on_change(sender, instance, **kwargs):
    update_search_index.delay()
