from django.conf.urls import url

from oscar.apps.dashboard.catalogue import app
from oscar.core.loading import get_class


class CatalogueApplication(app.CatalogueApplication):

    # Artist views
    artist_create_view = get_class(
        'dashboard.catalogue.views', 'ArtistCreateView'
    )
    artist_update_view = get_class(
        'dashboard.catalogue.views', 'ArtistUpdateView'
    )
    artist_list_view = get_class(
        'dashboard.catalogue.views', 'ArtistListView'
    )
    artist_delete_view = get_class(
        'dashboard.catalogue.views', 'ArtistDeleteView'
    )

    # Genre Views
    genre_create_view = get_class(
        'dashboard.catalogue.views', 'GenreCreateView'
    )
    genre_update_view = get_class(
        'dashboard.catalogue.views', 'GenreUpdateView'
    )
    genre_list_view = get_class(
        'dashboard.catalogue.views', 'GenreListView'
    )
    genre_delete_view = get_class(
        'dashboard.catalogue.views', 'GenreDeleteView'
    )

    def get_urls(self):
        urls = super(CatalogueApplication, self).get_urls()

        urls += [
            url(r'^artist/create/$',
                self.artist_create_view.as_view(),
                name='catalogue-artist-create'),
            url(r'^artists/$',
                self.artist_list_view.as_view(),
                name='catalogue-artist-list'),
            url(r'^artist/(?P<pk>\d+)/update/$',
                self.artist_update_view.as_view(),
                name='catalogue-artist-update'),
            url(r'^artist/(?P<pk>\d+)/delete/$',
                self.artist_delete_view.as_view(),
                name='catalogue-artist-delete'),
            url(r'^genre/create/$',
                self.genre_create_view.as_view(),
                name='catalogue-genre-create'),
            url(r'^genres/$',
                self.genre_list_view.as_view(),
                name='catalogue-genre-list'),
            url(r'^genre/(?P<pk>\d+)/update/$',
                self.genre_update_view.as_view(),
                name='catalogue-genre-update'),
            url(r'^genre/(?P<pk>\d+)/delete/$',
                self.genre_delete_view.as_view(),
                name='catalogue-genre-delete'),
        ]
        return self.post_process_urls(urls)


application = CatalogueApplication()
