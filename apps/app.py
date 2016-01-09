# -*- coding: utf-8 -*-
from oscar.app import Shop

from apps.checkout.app import application as checkout_app


class PayPalShop(Shop):
    checkout_app = checkout_app


application = PayPalShop()
