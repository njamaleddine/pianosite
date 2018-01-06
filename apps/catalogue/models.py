# -*- coding: utf-8 -*-
# Catalogue models
import uuid

import filetype
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from oscar.apps.catalogue.abstract_models import AbstractProduct

from apps.utility.files import upload_file
from apps.utility.models import TimeStampedModel
from .tasks import create_audio_samples
from .tasks import create_audio_samples_for_midi
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
    full_audio = models.FileField(
        upload_to=upload_file,
        max_length=1024,
        blank=True,
        null=True,
        help_text=_(
            'The full audio for an audio file, this field will be automatically set.'
        )
    )
    sample_ogg = models.FileField(
        upload_to=upload_file,
        max_length=1024,
        blank=True,
        null=True,
        help_text=_(
            'The sample ogg audio for an audio file, this field will be automatically set.'
        )
    )
    sample_mp3 = models.FileField(
        upload_to=upload_file,
        max_length=1024,
        blank=True,
        null=True,
        help_text=_(
            'The sample audio for an audio file, this field will be automatically set.'
        )
    )

    @cached_property
    def original(self):
        try:
            return self.__class__.objects.get(pk=self.pk)
        except self.__class__.DoesNotExist:
            return None

    @property
    def mime_type(self):
        if self.upload._file:
            return getattr(filetype.guess(self.upload._file.read(1024)), 'mime', None)
        with open(self.upload.path, mode='rb') as product_file:
            return getattr(filetype.guess(product_file.read(1024)), 'mime', None)
        return None

    def is_available_for_digital_purchase(self):
        if self.mime_type == 'audio/midi' or self.mime_type in settings.MIDISHOP_AUDIO_MIME_TYPES:
            return bool(self.upload and self.sample_ogg and self.sample_mp3)
        return bool(self.upload)

    def upload_has_changed(self):
        return not self.original or self.upload != self.original.upload

    def product_class_has_changed(self):
        return self.product_class.name.lower() != self.original.product_class.name.lower()

    def reset_fields(self):
        """
        Clear out audio fields so that changes in mime_type don't leave audio
        samples (ex. changing type)
        """
        self.full_audio = None
        self.sample_ogg = None
        self.sample_mp3 = None

    def clean(self, *args, **kwargs):
        if self.upload_has_changed() or self.product_class_has_changed():
            self.reset_fields()
        cleaned_data = super().clean(*args, **kwargs)

        if self.product_class.name.lower() == 'midi' and self.mime_type != 'audio/midi':
            raise ValidationError(
                _(
                    'You must upload a midi for a midi product. Change '
                    'the product type or upload a midi to continue.'
                )
            )

        if self.product_class.name.lower() == 'mp3' and self.mime_type != 'audio/mpeg':
            raise ValidationError(
                _(
                    'You must upload an mp3 for a mp3 product. Change '
                    'the product type or upload a mp3 to continue.'
                )
            )

        return cleaned_data

    def save(self, *args, **kwargs):
        original = self.original
        product = super().save(*args, **kwargs)

        if (not original or self.upload != original.upload) or not self.sample_ogg or not self.sample_mp3:
            if self.upload and self.mime_type == 'audio/midi':
                create_audio_samples_for_midi.delay(self.pk)
            elif self.upload and self.mime_type in settings.MIDISHOP_AUDIO_MIME_TYPES:
                create_audio_samples.delay(self.pk)
        return product


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
