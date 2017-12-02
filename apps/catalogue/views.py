# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.views.generic import View

from .models import MidiDownloadURL


class MidiDownloadView(View):
    def post(self, request, *args, **kwargs):
        """
        The view requires a `POST` request instead of a get request since
        prerendered page load should not count as a click to download the midi
        file

        If a user is not authenticated, an order_token must be passed in to
        redeem the order
        """
        uuid = self.kwargs.get('uuid')

        try:
            midi_download = MidiDownloadURL.objects.get(uuid=uuid)
        except MidiDownloadURL.DoesNotExist:
            midi_download = None

        if midi_download:
            if not midi_download.expired:
                if (
                    midi_download.owner == request.user or
                    (
                        midi_download.customer_email == request.POST.get('guest_email') and
                        request.user.is_anonymous()
                    )
                ):
                    # The user must be the owner of the download (authenticated)
                    # or if they purchased it as an unauthenticated user, their
                    # email must match the midi_download.customer_email
                    response = HttpResponse(
                        midi_download.file,
                        content_type='application/x-midi'
                    )
                    response['Content-Disposition'] = 'attachment; filename={}'.format(
                        midi_download.file_name
                    )

                    midi_download.date_redeemed = timezone.now()
                    midi_download.downloads_left -= 1
                    midi_download.save()
                    return response
                else:
                    # User must be authenticated to redeem; they purchased
                    # the midi as an authenticated user
                    return HttpResponseRedirect(reverse_lazy('customer:login'))
            else:
                messages.error(request, 'Your download has already been redeemed')
                return HttpResponseRedirect(
                    midi_download.product.get_absolute_url()
                )
        else:
            return HttpResponseRedirect(reverse_lazy('promotions:home'))


class MidiDownloadCancelView(View):
    """
    Sets the total remaining downloads to 0 for a given midi

    This view should only be accessible by an admin (is_staff & is_superuser)
    """
    def _response(self, request, *args, **kwargs):
        uuid = self.kwargs.get('uuid')
        order_number = self.kwargs.get('order_number')

        try:
            midi_download = MidiDownloadURL.objects.get(uuid=uuid)
        except MidiDownloadURL.DoesNotExist:
            midi_download = None

        if (
            midi_download and
            request.user.is_authenticated() and
            request.user.is_staff and
            request.user.is_superuser
        ):
            midi_download.date_redeemed = timezone.now()
            midi_download.downloads_left = 0
            midi_download.save()
            messages.success(request, 'The midi download has been deactivated')

        return HttpResponseRedirect(
            reverse_lazy('dashboard:order-detail', kwargs={'number': order_number})
        )

    def get(self, request, *args, **kwargs):
        # This is a fallback to the OrderDetailsView Override
        # This is mostly here for graceful degradation in case js is blocked
        # Though it's generally a bad idea to use GET for requests that mutate data
        return self._response(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._response(request, *args, **kwargs)
