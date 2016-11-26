from django.conf import settings

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def get_stripe_token(number, exp_month, exp_year, cvc):
    return stripe.Token.create(
        card={
            'number': number,
            'exp_month': exp_month,
            'exp_year': exp_year,
            'cvc': cvc
        },
    )
