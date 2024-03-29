from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class OrdersDashboardConfig(AppConfig):
    label = 'orders_dashboard'
    name = 'apps.dashboard.orders'
    verbose_name = _('Orders dashboard')
