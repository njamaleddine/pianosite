# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from djstripe.views import ChangeCardView as StripeChangeCardView


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
