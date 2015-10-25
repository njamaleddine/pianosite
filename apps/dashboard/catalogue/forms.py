from oscar.apps.dashboard.catalogue.forms import ProductForm as OscarProductForm


class ProductForm(OscarProductForm):

    class Meta (OscarProductForm.Meta):
        fields = [
            'title', 'upc', 'description', 'is_discountable', 'structure',
            'artist', 'genre', 'midi_file', 'sample_audio'
        ]
