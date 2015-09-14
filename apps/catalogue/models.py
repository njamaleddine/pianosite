# Catalogue models
import uuid

from django.auth import User
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible

from oscar.apps.catalogue.abstract_models import AbstractProduct

from apps.utility.toolbelt import upload_file
from apps.utility.process_midi import convert_to_audio, slice_audio

from signals import audio_slice_create


@python_2_unicode_compatible
class Artist (models.Model):
    name = models.CharField(max_length=255)

    class Meta (object):
        ordering = ("name",)

    def __str__(self):
        return u"{0}".format(self.name)


@python_2_unicode_compatible
class Genre (models.Model):
    name = models.CharField(max_length=255)

    class Meta (object):
        ordering = ("name",)

    def __str__(self):
        return u"{0}".format(self.name)


class Product (AbstractProduct):
    artist = models.ForeignKey(Artist, null=True, blank=True)
    genre = models.ForeignKey(Genre, null=True, blank=True)
    midi_file = models.FileField(upload_to=upload_file)
    sample_audio = models.URLField(max_length=2048, blank=True, null=True)

    def process_file_data(self):
        """
        Create audio slice from midi file
        Return path of sample_audio
        """
        if self.midi_file:
            output_filename = convert_to_audio(midi_filename=self.midi_file.name)
            slice_file_name = slice_audio(audio_file_name=output_filename)

            return u"{}/".format(settings.MEDIA_ROOT, slice_file_name)
        else:
            raise "No midi file available with this object"


post_save.connect(audio_slice_create, sender=Product)


@python_2_unicode_compatible
class MidiDownloadURL(models.Model):
    """ The midi download url available for the user to access the file """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product)
    owner = models.ForeignKey(User)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return u"{}".format(self.uuid)


from oscar.apps.catalogue.models import *
