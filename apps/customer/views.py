# -*- coding: utf-8 -*-

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from djstripe.views import ChangeCardView as StripeChangeCardView
from djstripe.views import LoginRequiredMixin, PaymentsContextMixin, DetailView
from djstripe.models import Customer

from djstripe.settings import subscriber_request_callback
import stripe

from apps.customer.utils import delete_all_stripe_cards


class ChangeCardView(StripeChangeCardView):
    """TODO: Needs to be refactored to leverage forms and context data."""
    template_name = "djstripe/change_card.html"
    context = {}

    def get_context_data(self, *args, **kwargs):
        context = super(ChangeCardView, self).get_context_data(**kwargs)
        context['active_tab'] = 'creditcards'
        return context

    def get_post_success_url(self):
        """ Makes it easier to do custom dj-stripe integrations. """
        return reverse("customer:change-card")


class DeleteCardView(LoginRequiredMixin, PaymentsContextMixin, DetailView):
    """TODO: Needs to be refactored to leverage forms and context data."""
    template_name = "djstripe/change_card.html"

    def get_object(self):
        if hasattr(self, "customer"):
            return self.customer
        self.customer, created = Customer.get_or_create(
            subscriber=subscriber_request_callback(self.request))
        return self.customer

    def post(self, request, *args, **kwargs):
        """
        TODO: Raise a validation error when a stripe token isn't passed.
            Should be resolved when a form is used.
        """

        customer = self.get_object()
        try:
            send_invoice = customer.card_fingerprint == ""
            if send_invoice:
                customer.send_invoice()
            customer.retry_unpaid_invoices()

            # Delete all cards for this user
            # (they can only have 1 card right now anyway)
            delete_all_stripe_cards(customer)

        except stripe.StripeError as exc:
            Customer.objects.filter(id=customer.pk).delete()
            messages.info(request, "Error removing deleting, please try again")
            return render(
                request,
                self.template_name,
                {
                    "customer": self.get_object(),
                    "stripe_error": str(exc)
                }
            )
        messages.info(request, "Your card has been removed from your account.")
        return redirect(self.get_post_success_url())

    def get_post_success_url(self):
        """ Makes it easier to do custom dj-stripe integrations. """
        return reverse("customer:change-card")
