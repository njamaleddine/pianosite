# Required to import the rest of the oscar models unfortunately
from django.db import models
from django.utils.translation import ugettext_lazy as _
from oscar.apps.payment.abstract_models import AbstractBankcard


class Bankcard(AbstractBankcard):
    stripe_token = models.CharField(_("Stripe Token"), max_length=500)


# Required to import the rest of the oscar models unfortunately
from oscar.apps.payment.models import *
