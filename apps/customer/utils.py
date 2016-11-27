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


def delete_all_stripe_cards(djstripe_customer):
    """
    All cards are deleted for the user,
    Since the user should only ever have one card, this will delete only their
    current card
    """
    sources = djstripe_customer.api_retrieve().sources

    customer = stripe.Customer.retrieve(djstripe_customer.stripe_id)
    for source in sources:
        customer.sources.retrieve(source['id']).delete()

    # Wipe the current fields after we delete the source (active card)
    djstripe_customer.card_fingerprint = ''
    djstripe_customer.card_last_4 = ''
    djstripe_customer.card_kind = ''
    djstripe_customer.card_exp_month = None
    djstripe_customer.card_exp_year = None
    djstripe_customer.save()
