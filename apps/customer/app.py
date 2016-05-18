# -*- coding: utf-8 -*-
from django.conf.urls import url

from oscar.apps.customer import app
from oscar.core.loading import get_class


class CustomerApplication(app.CustomerApplication):

    ChangeCardView = get_class(
        'customer.views', 'ChangeCardView'
    )

    def get_urls(self):
        urls = super(CustomerApplication, self).get_urls()

        urls += [
            url(r'^change_card',
                self.ChangeCardView.as_view(),
                name='change-card'),
        ]
        return self.post_process_urls(urls)


application = CustomerApplication()
