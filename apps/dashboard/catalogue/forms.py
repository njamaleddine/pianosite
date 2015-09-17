from oscar.apps.dashboard.catalogue.forms import ProductForm as OscarProductForm

from pianosite.apps.catalogue.models import Product


class ProductForm(OscarProductForm):

    class Meta (OscarProductForm.Meta):
        model = Product
        fields = [
            'title', 'upc', 'description', 'is_discountable', 'structure',
            'artist', 'genre', 'midi_file', 'sample_audio'
        ]
