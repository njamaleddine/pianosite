from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from oscar.apps.dashboard.orders.views import *


class OrderDetailView(OrderDetailView):
    """
    Dashboard view to display a single order.

    Supports the permission-based dashboard.

    Overrides the default action to allow the cancel_midi_download action
    """
    def post(self, request, *args, **kwargs):
        # For POST requests, we use a dynamic dispatch technique where a
        # parameter specifies what we're trying to do with the form submission.
        # We distinguish between order-level actions and line-level actions.

        order = self.object = self.get_object()

        if 'uuid' in request.POST and 'order_number' in request.POST and 'cancel_midi_download' in request.POST:
            # This is hacky, using the POST data to forward to a GET to deactivate the midi
            # But I am too lazy to handle it through a pure POST (can't embed a form in a form)
            # Best alternative would be ajax or an `order_action` in request.POST since only
            # POSTs should modify the backend, not GET requests. This is ok for now though
            return HttpResponseRedirect(
                reverse(
                    'catalogue:catalogue_cancel_midi_download',
                    kwargs={'order_number': request.POST['order_number'], 'uuid': request.POST['uuid']}
                )
            )

        # Look for order-level action first
        if 'order_action' in request.POST:
            return self.handle_order_action(
                request, order, request.POST['order_action'])

        # Look for line-level action
        if 'line_action' in request.POST:
            return self.handle_line_action(
                request, order, request.POST['line_action'])

        return self.reload_page(error=_("No valid action submitted"))
