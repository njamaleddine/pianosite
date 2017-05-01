# -*- coding: utf-8 -*-
from django.conf.urls import url

from oscar.apps.catalogue import app
from oscar.core.loading import get_class


class CatalogueApplication(app.CatalogueApplication):

    MidiDownloadView = get_class(
        'catalogue.views', 'MidiDownloadView'
    )
    MidiDownloadCancelView = get_class(
        'catalogue.views', 'MidiDownloadCancelView'
    )

    def get_urls(self):
        urls = super(CatalogueApplication, self).get_urls()

        urls += [
            url(r'^download/(?P<uuid>[^/]+)/$',
                self.MidiDownloadView.as_view(),
                name='catalogue_midi_download'),
            url(r'^cancel_download/(?P<uuid>[^/]+)/(?P<order_number>[\d]+)$',
                self.MidiDownloadCancelView.as_view(),
                name='catalogue_cancel_midi_download'),
        ]
        return self.post_process_urls(urls)


application = CatalogueApplication()
