from oscar.core.loading import get_class

from oscar.apps.dashboard.orders.app import OrdersDashboardApplication as OscarOrdersDashboardApplication


class OrdersDashboardApplication(OscarOrdersDashboardApplication):
    order_detail_view = get_class('apps.dashboard.orders.views', 'OrderDetailView')

    def get_urls(self):
        urls = super(OrdersDashboardApplication, self).get_urls()
        return self.post_process_urls(urls)


application = OrdersDashboardApplication()
