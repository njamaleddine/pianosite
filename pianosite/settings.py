"""
Django settings for pianosite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from collections import OrderedDict

import dj_database_url

from django.utils.translation import ugettext_lazy as _

# Oscar Imports
from oscar import get_core_apps
from oscar import OSCAR_MAIN_TEMPLATE_DIR
from oscar.defaults import *

from apps.utility.toolbelt import coerce_bool

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def location(path_name):
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)), path_name
    )


def append_to_base_dir(path):
    return os.path.join(BASE_DIR, path)

# Project specific information
SITE_NAME = u"Midi Shop"
SITE_ID = 1  # Necessary for Oscar

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = coerce_bool(os.environ.get("DEBUG", True))

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'widget_tweaks',
    'compressor',
    'paypal',
    'djstripe'
] + get_core_apps([
    'apps.catalogue',
    'apps.checkout',
    'apps.customer',
    'apps.dashboard',
    'apps.dashboard.catalogue',
    'apps.dashboard.promotions',
])

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # location('templates'),
            os.path.abspath("templates"),
            OSCAR_MAIN_TEMPLATE_DIR,
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'debug': coerce_bool(os.environ.get("TEMPLATE_DEBUG", DEBUG)),
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                "django.core.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.static",
                "django.core.context_processors.tz",

                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.promotions.context_processors.promotions',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
                'pianosite.context_processors.site_name',
                'pianosite.context_processors.contact_email',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                # needed by django-treebeard for admin (and potentially other libs)
                'django.template.loaders.eggs.Loader',
            ]
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

# DEBUG Toolbar
DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": coerce_bool(os.environ.get("TOOLBAR_INTERCEPT", False))
}

DEBUG_TOOLBAR = coerce_bool(os.environ.get("DEBUG_TOOLBAR", DEBUG))
if DEBUG_TOOLBAR:
    MIDDLEWARE_CLASSES += ("debug_toolbar.middleware.DebugToolbarMiddleware",)
    INSTALLED_APPS += ("debug_toolbar",)


ROOT_URLCONF = 'pianosite.urls'

WSGI_APPLICATION = 'pianosite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    }
}

if os.environ.get("DATABASE_URL", None):
    DATABASES['default'] = dj_database_url.config()

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
DEFAULT_FILE_STORAGE = os.environ.get(
    "DEFAULT_FILE_STORAGE",
    "django.core.files.storage.FileSystemStorage"
)

STATIC_URL = '/static/'
STATIC_ROOT = location('public/static')
STATICFILES_DIRS = (
    # location('static/'),
    append_to_base_dir('static/'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
# Media URL
MEDIA_ROOT = location("public/media")
MEDIA_URL = os.environ.get("MEDIA_URL", "/media/")

# Email
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", None)
SERVER_EMAIL = "server@midishop.com"
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", None)
EMAIL_HOST = os.environ.get("EMAIL_HOST", None)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", None)
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", None)
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 25))

if EMAIL_PORT:
    EMAIL_USE_TLS = True

# Oscar Settings
OSCAR_SHOP_NAME = u"{}".format(SITE_NAME)
OSCAR_SHOP_TAGLINE = ""
OSCAR_FROM_EMAIL = SERVER_EMAIL
OSCAR_DEFAULT_CURRENCY = "USD"
OSCAR_ALLOW_ANON_CHECKOUT = True

OSCAR_DASHBOARD_NAVIGATION = [
    {
        'label': _('Dashboard'),
        'icon': 'icon-th-list',
        'url_name': 'dashboard:index',
    },
    {
        'label': _('Catalogue'),
        'icon': 'icon-sitemap',
        'children': [
            {
                'label': _('Products'),
                'url_name': 'dashboard:catalogue-product-list',
            },
            {
                'label': _('Product Types'),
                'url_name': 'dashboard:catalogue-class-list',
            },
            {
                'label': _('Categories'),
                'url_name': 'dashboard:catalogue-category-list',
            },
            {
                'label': _('Ranges'),
                'url_name': 'dashboard:range-list',
            },
            {
                'label': _('Low stock alerts'),
                'url_name': 'dashboard:stock-alert-list',
            },
            {
                'label': _('Artists'),
                'url_name': 'dashboard:catalogue-artist-list',
            },
            {
                'label': _('Genres'),
                'url_name': 'dashboard:catalogue-genre-list',
            },
        ]
    },
    {
        'label': _('Fulfilment'),
        'icon': 'icon-shopping-cart',
        'children': [
            {
                'label': _('Orders'),
                'url_name': 'dashboard:order-list',
            },
            {
                'label': _('Statistics'),
                'url_name': 'dashboard:order-stats',
            },
            {
                'label': _('Partners'),
                'url_name': 'dashboard:partner-list',
            },
            # The shipping method dashboard is disabled by default as it might
            # be confusing. Weight-based shipping methods aren't hooked into
            # the shipping repository by default (as it would make
            # customising the repository slightly more difficult).
            # {
            #     'label': _('Shipping charges'),
            #     'url_name': 'dashboard:shipping-method-list',
            # },
        ]
    },
    {
        'label': _('Customers'),
        'icon': 'icon-group',
        'children': [
            {
                'label': _('Customers'),
                'url_name': 'dashboard:users-index',
            },
            {
                'label': _('Stock alert requests'),
                'url_name': 'dashboard:user-alert-list',
            },
        ]
    },
    {
        'label': _('Offers'),
        'icon': 'icon-bullhorn',
        'children': [
            {
                'label': _('Offers'),
                'url_name': 'dashboard:offer-list',
            },
            {
                'label': _('Vouchers'),
                'url_name': 'dashboard:voucher-list',
            },
        ],
    },
    {
        'label': _('Content'),
        'icon': 'icon-folder-close',
        'children': [
            {
                'label': _('Content blocks'),
                'url_name': 'dashboard:promotion-list',
            },
            {
                'label': _('Content blocks by page'),
                'url_name': 'dashboard:promotion-list-by-page',
            },
            {
                'label': _('Pages'),
                'url_name': 'dashboard:page-list',
            },
            {
                'label': _('Email templates'),
                'url_name': 'dashboard:comms-list',
            },
            {
                'label': _('Reviews'),
                'url_name': 'dashboard:reviews-list',
            },
        ]
    },
    {
        'label': _('Reports'),
        'icon': 'icon-bar-chart',
        'url_name': 'dashboard:reports-index',
    },
    {
        'label': _('PayPal'),
        'icon': 'icon-globe',
        'children': [
            {
                'label': _('Express transactions'),
                'url_name': 'paypal-express-list',
            },
        ]
    }
]
OSCAR_SEARCH_FACETS = {
    'fields': OrderedDict([
        ('product_class', {'name': _('Type'), 'field': 'product_class'}),
        ('rating', {'name': _('Rating'), 'field': 'rating'}),
    ]),
    'queries': OrderedDict([
        ('price_range',
         {
             'name': _('Price range'),
             'field': 'price',
             'queries': [
                 # This is a list of (name, query) tuples where the name will
                 # be displayed on the front-end.
                 (_('0 to 20'), u'[0 TO 20]'),
                 (_('20 to 40'), u'[20 TO 40]'),
                 (_('40 to 60'), u'[40 TO 60]'),
                 (_('60+'), u'[60 TO *]'),
             ]
         }),
    ]),
}
OSCAR_MISSING_IMAGE_URL = append_to_base_dir('pianosite/public/media/placeholder.png')

# Oscar Paypal Support
PAYPAL_API_USERNAME = os.environ.get("PAYPAL_API_USERNAME", "")
PAYPAL_API_PASSWORD = os.environ.get("PAYPAL_API_PASSWORD", "")
PAYPAL_API_SIGNATURE = os.environ.get("PAYPAL_API_SIGNATURE", "")
# Taken from PayPal's documentation - these should always work in the sandbox
PAYPAL_SANDBOX_MODE = coerce_bool(os.environ.get("PAYPAL_SANDBOX_MODE", True))
PAYPAL_CALLBACK_HTTPS = False
PAYPAL_API_VERSION = '88.0'
PAYPAL_CURRENCY = PAYPAL_PAYFLOW_CURRENCY = "USD"

PAYPAL_PAYFLOW_DASHBOARD_FORMS = True

# Paypal Payflow
PAYPAL_PAYFLOW_PARTNER = os.environ.get("PAYPAL_PAYFLOW_PARTNER", "PayPal")
PAYPAL_PAYFLOW_VENDOR_ID = os.environ.get("PAYPAL_PAYFLOW_VENDOR_ID", "")
PAYPAL_PAYFLOW_PASSWORD = os.environ.get("PAYPAL_PAYFLOW_PASSWORD", "")
PAYPAL_PAYFLOW_PRODUCTION_MODE = DEBUG

LANGUAGES = (
    ('en-us', _('English')),
    # ('es', _('Spanish')),
)

# DJ-STRIPE
STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
