# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf import settings


def contact_email(request):
    return {"contact_email": settings.CONTACT_EMAIL}


def site_name(request):
    return {"site_name": settings.SITE_NAME}
