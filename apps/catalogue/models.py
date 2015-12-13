# Catalogue models
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible

from oscar.apps.catalogue.abstract_models import AbstractProduct

from apps.utility.toolbelt import upload_file, get_file_name_from_path
from apps.utility.process_midi import convert_to_audio, slice_audio

from pianosite.settings import BASE_DIR

from signals import audio_creation


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
    midi_file = models.FileField(upload_to=upload_file, max_length=1024)
    full_audio = models.FileField(upload_to=upload_file, max_length=1024, blank=True, null=True)
    sample_audio = models.FileField(upload_to=upload_file, max_length=1024, blank=True, null=True)

    def audio_conversion(self):
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

            audio_url = u'{}{}'.format(audio_base_url, audio_filename)
            audio_slice_url = u'{}{}'.format(
                audio_base_url, get_file_name_from_path(slice_file_name)
            )
            return audio_url, audio_slice_url
        else:
            raise "No midi file available with this object"

    def save(self, *args, **kwargs):
        return super(Product, self).save(*args, **kwargs)

post_save.connect(audio_creation, sender=Product)


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
