# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.db import migrations


def create_product_classes(apps, schema_editor):
    ProductClass = apps.get_app_config('catalogue').models.get('productclass')
    ProductClass.objects.get_or_create(
        name='Midi',
        requires_shipping=False,
        track_stock=False
    )


def create_categories(apps, schema_editor):
    Category = apps.get_model("catalogue", "Category")
    try:
        category = Category.objects.get(path='0001')
    except:
        category = None

    if not category:
        Category.objects.get_or_create(
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


def create_partners(apps, schema_editor):
    Partner = apps.get_app_config('partner').models.get('partner')
    Partner.objects.get_or_create(
        name='MidiShop',
        code='midishop'
    )


def create_automatic_product_lists(apps, schema_editor):
    """ Generate Automatic product list """
    AutomaticProductList = apps.get_app_config('promotions').models.get('automaticproductlist')
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
    PagePromotion = apps.get_app_config('promotions').models.get('pagepromotion')

    automatic_product_list_content_type = ContentType.objects.get(app_label="promotions", model="automaticproductlist")

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


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0001_initial'),  # We need django-oscar to create the db table schema first
        ('catalogue', '0006_auto_20150921_0112'),
    ]

    operations = [
        migrations.RunPython(create_product_classes),
        migrations.RunPython(create_categories),
        migrations.RunPython(create_partners),
        migrations.RunPython(create_automatic_product_lists),
    ]
