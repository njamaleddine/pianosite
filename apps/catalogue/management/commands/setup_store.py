# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from apps.catalogue.models import Category
from apps.catalogue.models import ProductClass
from oscar.apps.partner.models import Partner
from oscar.apps.promotions.models import AutomaticProductList
from oscar.apps.promotions.models import PagePromotion


class Command(BaseCommand):
    help = 'Setup store with default data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up store data...'))

        self.create_product_classes()
        self.create_categories()
        self.create_partners()
        self.create_automatic_product_lists()

        self.stdout.write(self.style.SUCCESS('Store setup complete'))

    def create_product_classes(self):
        product_class, created = ProductClass.objects.get_or_create(
            name='Midi',
            requires_shipping=False,
            track_stock=False
        )
        return product_class

    def create_categories(self):
        try:
            category = Category.objects.get(path='0001')
        except Category.DoesNotExist:
            category = None

        if not category:
            category, created = Category.objects.get_or_create(
                slug='midi',
                name='Midi',
                path='0001',
                depth=1,
                numchild=0
            )
        else:
            category.name = 'Midi'
            category.slug = 'midi'
            category.depth = 1
            category.numchild = 0
            category.save()

        return category

    def create_partners(self):
        partner, created = Partner.objects.get_or_create(
            name='MidiShop',
            code='midishop'
        )
        return partner

    def create_automatic_product_lists(self):
        """ Generate Automatic product list """
        # Create Newest Products list
        new_items, created = AutomaticProductList.objects.get_or_create(
            name='New Items',
            method='RecentlyAdded',
            num_products=4
        )
        # Create best sellers product list
        best_sellers, created = AutomaticProductList.objects.get_or_create(
            name='Best Sellers',
            method='Bestselling',
            num_products=4
        )

        # Add the promotions to the homepage
        automatic_product_list_content_type = ContentType.objects.get(
            app_label="promotions",
            model="automaticproductlist"
        )

        PagePromotion.objects.get_or_create(
            page_url='/',
            content_type_id=automatic_product_list_content_type.id,
            object_id=new_items.id,
            position='page'
        )
        PagePromotion.objects.get_or_create(
            page_url='/',
            content_type_id=automatic_product_list_content_type.id,
            object_id=best_sellers.id,
            position='page'
        )
