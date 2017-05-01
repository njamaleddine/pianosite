# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

# Catalogue models
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from oscar.apps.basket.abstract_models import AbstractLine
from apps.catalogue.models import MidiDownloadURL


@python_2_unicode_compatible
class Line(AbstractLine):
    midi_download_url = models.ForeignKey(MidiDownloadURL, null=True, blank=True, related_name='basket_midi_download_url')


# Required to import the rest of the oscar models unfortunately
from oscar.apps.basket.models import *
