# -*- coding: utf-8 -*-
# Required to import the rest of the oscar models unfortunately
from oscar.apps.customer.models import *

from django.conf import settings
# from djstripe.models import Customer as DJStripeCustomer

User = settings.AUTH_USER_MODEL


# def customer_create_charge(request, amount):
#     """
#     Creates a stripe charge

#     amount (Decimal): The amount to charge the user
#     """
#     try:
#         user = User.objects.get(id=request.user.id)
#         customer, created = DJStripeCustomer.get_or_create(subscriber=user)
#         customer.charge(amount)
#     except User.DoesNotExist:
#         user = request.user
