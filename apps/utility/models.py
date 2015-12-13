# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDTimeStampedModel(UUIDModel, TimeStampedModel):

    class Meta:
        abstract = True


class ActiveModel(models.Model):
    """
    An abstract base class that provides a field for indicating whether an
    object is active or not.
    """
    is_active = models.BooleanField(
        default=True,
        help_text=_(
            'Designates whether this is considered active or not. '
            'Uncheck this instead of deleting if you want to preserve '
            'upvote (donation) records.'
        )
    )

    class Meta:
        abstract = True


class OrderedModel(models.Model):
    """
    An abstract base class that provides a field for indicating an object's
    rank/ordering
    """
    order = models.PositiveIntegerField(
        _("order"),
        default=0,
        help_text=_(
            "Indicates the ordering of the object. Lower numbers come first "
            "in ascending order. 0 = First."
        )
    )

    class Meta:
        abstract = True
