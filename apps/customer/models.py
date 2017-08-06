# -*- coding: utf-8 -*-
# Required to import the rest of the oscar models unfortunately
import stripe

from django.conf import settings
from django.db import models
from django.db.models.deletion import SET_NULL
from django.utils.translation import ugettext_lazy as _
from oscar.apps.customer.models import *  # noqa

from djstripe.stripe_objects import StripeCustomer
from djstripe.models import Charge


class GuestStripeCustomer(StripeCustomer):
    """ Anonymous User (Guest) used for creating charges during checkout """
    email = models.EmailField(_('email address'))
    default_source = models.ForeignKey(
        Charge,
        null=True,
        related_name="guest_customers",
        on_delete=SET_NULL
    )

    def can_charge(self):
        return self.has_valid_card()

    @classmethod
    def _api(cls):
        """
        Get the api object for this type of stripe object (requires
        stripe_api_name attribute to be set on model).
        """
        if cls.stripe_api_name is None:
            raise NotImplementedError("StripeObject descendants are required to define "
                                      "the stripe_api_name attribute")
        # e.g. stripe.Event, stripe.Charge, etc
        return getattr(stripe, cls.stripe_api_name)

    @classmethod
    def _api_create(cls, api_key=settings.STRIPE_SECRET_KEY, **kwargs):
        """
        Call the stripe API's create operation for this model.
        :param api_key: The api key to use for this request. Defualts to settings.STRIPE_SECRET_KEY.
        :type api_key: string
        """

        return cls._api().create(api_key=api_key, **kwargs)

    @classmethod
    def create(cls, email):
        stripe_customer = cls._api_create(email=email)
        customer, created = cls.objects.get_or_create(
            email=email,
            stripe_id=stripe_customer.id,
        )
        return customer

    def add_card(self, source, set_default=True):
        """
        Adds a card to this customer's account.
        :param source: Either a token, like the ones returned by our Stripe.js, or a dictionary containing a
                       user's credit card details. Stripe will automatically validate the card.
        :type source: string, dict
        :param set_default: Whether or not to set the source as the customer's default source
        :type set_default: boolean
        """

        stripe_customer = self.api_retrieve()
        stripe_card = stripe_customer.sources.create(source=source)

        if set_default:
            stripe_customer.default_source = stripe_card["id"]
            stripe_customer.save()

        return stripe_card
