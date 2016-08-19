# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from oscar.core.loading import get_model
from django.shortcuts import get_object_or_404, HttpResponseRedirect

from .forms import ArtistForm, GenreForm

Artist = get_model('catalogue', 'Artist')
Genre = get_model('catalogue', 'Genre')


class ArtistCreateUpdateView(generic.UpdateView):

    template_name = 'dashboard/catalogue/artist_form.html'
    model = Artist
    form_class = ArtistForm

    def forms_valid(self, form, attributes_formset):
        form.save()
        attributes_formset.save()

        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form, attributes_formset):
        messages.error(self.request,
                       _("Your submitted data was not valid - please "
                         "correct the errors below"
                         ))
        ctx = self.get_context_data(form=form,
                                    attributes_formset=attributes_formset)
        return self.render_to_response(ctx)

    def get_context_data(self, *args, **kwargs):
        ctx = super(ArtistCreateUpdateView, self).get_context_data(
            *args, **kwargs)
        return ctx


class ArtistCreateView(ArtistCreateUpdateView):

    creating = True

    def get_object(self):
        return None

    def get_title(self):
        return _("Add a new Artist")

    def get_success_url(self):
        messages.info(self.request, _("Artist created successfully"))
        return reverse("dashboard:catalogue-artist-list")


class ArtistUpdateView(ArtistCreateUpdateView):

    creating = False

    def get_title(self):
        return _("Update Artist '%s'") % self.object.name

    def get_success_url(self):
        messages.info(self.request, _("Artist updated successfully"))
        return reverse("dashboard:catalogue-artist-list")

    def get_object(self):
        artist = get_object_or_404(Artist, pk=self.kwargs['pk'])
        return artist


class ArtistListView(generic.ListView):
    template_name = 'dashboard/catalogue/artist_list.html'
    context_object_name = 'classes'
    model = Artist

    def get_context_data(self, *args, **kwargs):
        ctx = super(ArtistListView, self).get_context_data(*args, **kwargs)
        ctx['title'] = _("Artists")
        return ctx


class ArtistDeleteView(generic.DeleteView):
    template_name = 'dashboard/catalogue/artist_delete.html'
    model = Artist
    form_class = ArtistForm

    def get_context_data(self, *args, **kwargs):
        ctx = super(ArtistDeleteView, self).get_context_data(*args, **kwargs)
        ctx['title'] = _("Delete Artist '%s'") % self.object.name
        product_count = self.object.products.count()

        if product_count > 0:
            ctx['disallow'] = True
            ctx['title'] = _("Unable to delete '%s'") % self.object.name
            messages.error(self.request,
                           _("%i products are still assigned to this type") %
                           product_count)
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Artist deleted successfully"))
        return reverse("dashboard:catalogue-artist-list")


class GenreCreateUpdateView(generic.UpdateView):

    template_name = 'dashboard/catalogue/genre_form.html'
    model = Genre
    form_class = GenreForm

    def forms_valid(self, form, attributes_formset):
        form.save()
        attributes_formset.save()

        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form, attributes_formset):
        messages.error(self.request,
                       _("Your submitted data was not valid - please "
                         "correct the errors below"
                         ))
        ctx = self.get_context_data(form=form,
                                    attributes_formset=attributes_formset)
        return self.render_to_response(ctx)

    def get_context_data(self, *args, **kwargs):
        ctx = super(GenreCreateUpdateView, self).get_context_data(
            *args, **kwargs)
        return ctx


class GenreCreateView(GenreCreateUpdateView):

    creating = True

    def get_object(self):
        return None

    def get_title(self):
        return _("Add a new Genre")

    def get_success_url(self):
        messages.info(self.request, _("Genre created successfully"))
        return reverse("dashboard:catalogue-genre-list")


class GenreUpdateView(GenreCreateUpdateView):

    creating = False

    def get_title(self):
        return _("Update Genre '%s'") % self.object.name

    def get_success_url(self):
        messages.info(self.request, _("Genre updated successfully"))
        return reverse("dashboard:catalogue-genre-list")

    def get_object(self):
        genre = get_object_or_404(Genre, pk=self.kwargs['pk'])
        return genre


class GenreListView(generic.ListView):
    template_name = 'dashboard/catalogue/genre_list.html'
    context_object_name = 'classes'
    model = Genre

    def get_context_data(self, *args, **kwargs):
        ctx = super(GenreListView, self).get_context_data(*args, **kwargs)
        ctx['title'] = _("Genres")
        return ctx


class GenreDeleteView(generic.DeleteView):
    template_name = 'dashboard/catalogue/genre_delete.html'
    model = Genre
    form_class = GenreForm

    def get_context_data(self, *args, **kwargs):
        ctx = super(GenreDeleteView, self).get_context_data(*args, **kwargs)
        ctx['title'] = _("Delete Genre '%s'") % self.object.name
        product_count = self.object.products.count()

        if product_count > 0:
            ctx['disallow'] = True
            ctx['title'] = _("Unable to delete '%s'") % self.object.name
            messages.error(self.request,
                           _("%i products are still assigned to this type") %
                           product_count)
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Genre deleted successfully"))
        return reverse("dashboard:catalogue-genre-list")

from oscar.apps.dashboard.catalogue.views import *
