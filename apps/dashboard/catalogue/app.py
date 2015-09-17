from oscar.apps.dashboard.catalogue import app

from apps.dashboard.catalogue import views


class CatalogueApplication(app.CatalogueApplication):
    payment_details_view = views.PaymentDetailsView


application = CatalogueApplication()
