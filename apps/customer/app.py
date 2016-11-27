# -*- coding: utf-8 -*-
from django.conf.urls import url

from oscar.apps.customer import app
from oscar.core.loading import get_class


class CustomerApplication(app.CustomerApplication):

    ChangeCardView = get_class(
        'customer.views', 'ChangeCardView'
    )
    DeleteCardView = get_class(
        'customer.views', 'DeleteCardView'
    )

    def get_urls(self):
        urls = super(CustomerApplication, self).get_urls()

        urls += [
            url(r'^change_card',
                self.ChangeCardView.as_view(),
                name='change-card'),
            url(r'^delete_card',
                self.DeleteCardView.as_view(),
                name='delete-card'),
        ]
        return self.post_process_urls(urls)


application = CustomerApplication()
