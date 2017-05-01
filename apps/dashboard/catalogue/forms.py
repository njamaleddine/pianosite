from django import forms

from oscar.apps.dashboard.catalogue.forms import ProductForm as OscarProductForm
from oscar.core.loading import get_model

Artist = get_model('catalogue', 'Artist')
Genre = get_model('catalogue', 'Genre')


class ProductForm(OscarProductForm):

    class Meta (OscarProductForm.Meta):
        fields = [
            'title', 'upc', 'description', 'is_discountable', 'structure',
            'artist', 'genre', 'midi_file', 'full_audio', 'sample_ogg',
            'sample_mp3'
        ]


class ArtistForm(forms.ModelForm):

    class Meta:
        model = Artist
        fields = ['name']


class GenreForm(forms.ModelForm):

    class Meta:
        model = Genre
        fields = ['name']
