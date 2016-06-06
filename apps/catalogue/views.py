# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
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

        if request.user.is_authenticated():
            try:
                midi_download = MidiDownloadURL.objects.get(uuid=uuid, owner=request.user)
            except:
                midi_download = None

            if midi_download:
                if not midi_download.expired:
                    response = HttpResponse(
                        midi_download.file,
                        content_type='application/x-midi'
                    )
                    response['Content-Disposition'] = 'attachment; filename={}'.format(
                        midi_download.file_name
                    )

                    midi_download.date_redeemed = timezone.now()
                    midi_download.save()
                    return response
                else:
                    messages.error(request, 'Your download has already been redeemed')
                    return HttpResponseRedirect(
                        midi_download.product.get_absolute_url()
                    )
            else:
                return HttpResponseRedirect(reverse_lazy('promotions:home'))
        else:
            # User must be authenticated to redeem
            return HttpResponseRedirect(reverse_lazy('customer:login'))
