from django.conf.urls import url

from oscar.apps.catalogue import app
from oscar.core.loading import get_class


class CatalogueApplication(app.CatalogueApplication):

    # Artist views
    MidiDownloadView = get_class(
        'catalogue.views', 'MidiDownloadView'
    )

    def get_urls(self):
        urls = super(CatalogueApplication, self).get_urls()

        urls += [
            url(r'^download/(?P<uuid>[^/]+)/$',
                self.MidiDownloadView.as_view(),
                name='catalogue_midi_download'),
        ]
        return self.post_process_urls(urls)


application = CatalogueApplication()
