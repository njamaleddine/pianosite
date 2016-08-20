from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from apps.app import application

from paypal.payflow.dashboard.app import application as payflow
from paypal.express.dashboard.app import application as express_dashboard


urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # The Django admin is not officially supported; expect breakage.
    # Nonetheless, it's often useful for debugging.
    url(r'^admin/', include(admin.site.urls)),

    # PayPal Express integration...
    url(r'^checkout/paypal/', include('paypal.express.urls')),
    # Dashboard views for Payflow Pro
    url(r'^dashboard/paypal/payflow/', include(payflow.urls)),
    # Dashboard views for Express
    url(r'^dashboard/paypal/express/', include(express_dashboard.urls)),

    url(r'', include(application.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
