# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from oscar.apps.checkout import views
from djstripe.models import Customer as DJStripeCustomer

from apps.catalogue.models import MidiDownloadURL
from apps.customer.models import GuestStripeCustomer
from apps.payment import forms
from apps.payment.models import SourceType


User = get_user_model()

logger = logging.getLogger(__name__)


class PaymentDetailsView(views.PaymentDetailsView):

    def get_context_data(self, **kwargs):
        # Override method so the bankcard form can be added to the context.
        ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)
        ctx['bankcard_form'] = kwargs.get('bankcard_form', forms.BankcardForm())
        ctx['STRIPE_PUBLIC_KEY'] = settings.STRIPE_PUBLIC_KEY

        # Get or create a new customer if the user is authenticated
        ctx['customer'] = None
        if self.request.user.is_authenticated():
            user = self.request.user
            customer, created = DJStripeCustomer.get_or_create(subscriber=user)
            ctx['customer'] = customer
        return ctx

    def get(self, request, *args, **kwargs):
        # Skip if the user is authenticated and has a valid stripe credit card
        ctx = self.get_context_data()
        customer = ctx['customer']
        if customer and customer.can_charge():
            # Don't show the bank card form if the customer is authenticated
            return self.render_preview(request, bankcard_form=None)
        return super(PaymentDetailsView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Override so we can validate the bankcard submission.
        # If it is valid, we render the preview screen with the forms hidden
        # within it.  When the preview is submitted, we pick up the 'action'
        # parameters and actually place the order.
        if request.POST.get('action', '') == 'place_order':
            return self.do_place_order(request)

        bankcard_form = forms.BankcardForm(request.POST)
        ctx = self.get_context_data(bankcard_form=bankcard_form)

        if not bankcard_form.is_valid():
            # Form validation failed, render page again with errors
            self.preview = False
            return self.render_to_response(ctx)

        # Render preview with bankcard details hidden
        return self.render_preview(request, bankcard_form=bankcard_form)

    def do_place_order(self, request):
        # Helper method to check that the hidden forms wasn't tinkered
        # with.
        ctx = self.get_context_data()
        customer = ctx['customer']

        if customer and customer.can_charge():
            submission = self.build_submission()
            return self.submit(**submission)

        bankcard_form = forms.BankcardForm(request.POST)
        if not bankcard_form.is_valid():
            messages.error(request, "Invalid submission")
            return HttpResponseRedirect(reverse('checkout:payment-details'))

        # Attempt to submit the order, passing the bankcard object so that it
        # gets passed back to the 'handle_payment' method below.
        submission = self.build_submission()
        submission['payment_kwargs']['bankcard'] = bankcard_form.bankcard
        return self.submit(**submission)

    def get_stripe_metadata(self, order_number, basket):
        metadata = {
            'dashboard_order_url': self.request.build_absolute_uri(
                reverse('dashboard:order-detail', kwargs={'number': order_number})
            ),
            'order_number': order_number,
            'total': basket.total_incl_tax,
        }
        return metadata

    def payment_description(self, order_number, total, email, **kwargs):
        return (
            'Order {order_number} with a total of {total} for {email}'.format(
                order_number=order_number,
                total=total.incl_tax,
                email=email,
            )
        )

    def handle_payment(self, order_number, total, **kwargs):
        """
        Make submission to Stripe
        """
        ctx = self.get_context_data()
        customer = ctx['customer']
        guest_email = ctx.get('guest_email')
        bankcard = kwargs.get('bankcard')

        # Record payment source and event
        # stripe_ref = Facade().charge(
        #     order_number, total, card=self.request.POST['STRIPE_TOKEN'],
        #     description=self.payment_description(order_number, total, **kwargs),
        #     metadata=self.payment_metadata(order_number, total, **kwargs)
        # )
        source_type, is_created = SourceType.objects.get_or_create(name='Stripe')
        source = source_type.sources.model(
            source_type=source_type,
            amount_allocated=total.incl_tax, currency=total.currency,
            amount_debited=total.incl_tax)  # , reference=stripe_ref)
        self.add_payment_source(source)

        # Create the charge on stripe
        try:
            if customer and customer.can_charge():
                customer.charge(
                    amount=total.incl_tax,
                    currency='usd',
                    description=self.payment_description(
                        order_number, total, customer.subscriber.email, **kwargs
                    ),
                    metadata=self.get_stripe_metadata(order_number, ctx['basket'])
                )
            elif guest_email and bankcard and bankcard.stripe_token:
                guest_customer = GuestStripeCustomer.create(email=guest_email)
                guest_customer.add_card(
                    source=bankcard.stripe_token
                )
                guest_customer.charge(
                    amount=total.incl_tax,
                    currency='usd',
                    description=self.payment_description(
                        order_number, total, guest_email, **kwargs
                    ),
                    metadata=self.get_stripe_metadata(order_number, ctx['basket'])
                )
            else:
                raise ValidationError('Unable to make charge, credit card is invalid')
        except Exception as e:
            # Some invalid card error here
            raise ValidationError(str(e))
        self.add_payment_event('charge-created', total.incl_tax)

    def create_midi_download_urls(self, user, basket):
        """
        Creates midi download urls for each product in the basket

        params
            user: request.user
            basket: basket instance
        """
        customer = None
        if user.is_authenticated():
            customer = user
            customer_email = user.email
        else:
            customer_email = self.get_context_data()['guest_email']

        midi_download_urls = []

        basket_lines = basket.lines.all()

        for line in basket_lines:
            midi_download_urls.append(
                MidiDownloadURL(
                    product=line.product,
                    owner=customer,
                    customer_email=customer_email,
                    downloads_left=line.quantity,
                )
            )

        created_midi_download_urls = MidiDownloadURL.objects.bulk_create(midi_download_urls)

        for index, line in enumerate(basket_lines):
            line.midi_download_url = created_midi_download_urls[index]
            line.save()

    def submit(self, user, basket, shipping_address, shipping_method,  # noqa (too complex (10))
               shipping_charge, billing_address, order_total,
               payment_kwargs=None, order_kwargs=None):
        self.create_midi_download_urls(user, basket)

        return super(PaymentDetailsView, self).submit(
            user, basket, shipping_address, shipping_method,
            shipping_charge, billing_address, order_total,
            payment_kwargs, order_kwargs
        )
