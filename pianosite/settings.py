"""
Django settings for pianosite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from collections import OrderedDict

import dj_database_url
import environ

from celery.schedules import crontab
from django.utils.translation import ugettext_lazy as _
from oscar import get_core_apps
from oscar import OSCAR_MAIN_TEMPLATE_DIR
from oscar.defaults import *  # noqa
from pianosite import __version__


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
env = environ.Env()


def location(path_name):
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)), path_name
    )


def append_to_base_dir(path):
    return os.path.join(BASE_DIR, path)


# Project specific information
# Django Sites Framework
SITE_SCHEME = env('SITE_SCHEME', default='http')
SITE_NAME = env('SITE_NAME', default='Midi Shop')
SITE_DOMAIN = env('SITE_DOMAIN', default='midisonline.com')
SITE_ID = env.int('SITE_ID', default=1)  # Necessary for Oscar

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', default=None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django_extensions',
    'widget_tweaks',
    'compressor',
    'djstripe',
] + get_core_apps([
    'apps.basket',
    'apps.catalogue',
    'apps.checkout',
    'apps.customer',
    'apps.dashboard',
    'apps.order',
    'apps.payment',
    'apps.search',
    'apps.dashboard.catalogue',
    'apps.dashboard.orders',
])

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Ensure a valid basket is added to the request instance for every request
    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.abspath('templates'),
            OSCAR_MAIN_TEMPLATE_DIR,
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'debug': env.bool('TEMPLATE_DEBUG', default=DEBUG),
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',

                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.promotions.context_processors.promotions',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
                'pianosite.context_processors.site_name',
                'pianosite.context_processors.contact_email',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    # needed by django-treebeard for admin (and potentially other libs)
                    'django.template.loaders.eggs.Loader',
                ]),
            ]
        },
    },
]

# SECURITY
# -----------------------------------------------------------------------------
# Allow javascripts to read CSRF token from cookies
CSRF_COOKIE_HTTPONLY = False
# Do not allow Session cookies to be read by javascript
SESSION_COOKIE_HTTPONLY = True

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

if SITE_SCHEME == 'https':
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://localhost:8983/solr',
        'INCLUDE_SPELLING': True,
    },
}

ROOT_URLCONF = 'pianosite.urls'

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
# -----------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': env.int('DATABASE_CONN_MAX_AGE', default=60)
    }
}

if env('DATABASE_URL', default=None):
    DATABASES['default'] = dj_database_url.config()

# CACHES
# -----------------------------------------------------------------------------
CACHES = {
    'default': env.cache('CACHE_URL', default='redis://127.0.0.1:6379/0'),
}

# SESSIONS
# -----------------------------------------------------------------------------
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = "default"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
# -----------------------------------------------------------------------------
DEFAULT_FILE_STORAGE = os.environ.get(
    'DEFAULT_FILE_STORAGE',
    'django.core.files.storage.FileSystemStorage'
)
STATIC_URL = '/static/'
STATIC_ROOT = location('public/static')
STATICFILES_DIRS = (
    append_to_base_dir('static/'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Media
# -----------------------------------------------------------------------------
MEDIA_ROOT = location('public/media')
MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')

# Celery
# -----------------------------------------------------------------------------
BROKER_URL = env('BROKER_URL', default='redis://127.0.0.1:6379')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERYD_HIJACK_ROOT_LOGGER = False

# Scheduled Tasks
CELERYBEAT_SCHEDULE = {
    'search-rebuild-index': {
        'task': 'apps.catalogue.tasks.rebuild_search_index',
        'schedule': crontab(hour=7, minute=00),
    },
}

# MidiShop Settings
# -----------------------------------------------------------------------------
MIDISHOP_AUDIO_SAMPLE_LENGTH = env.int('MIDISHOP_AUDIO_SAMPLE_LENGTH', default=30)  # in seconds
MIDISHOP_SOUNDFONT_PATH = env(
    'MIDISHOP_DEFAULT_SOUNDFONT_PATH',
    default=append_to_base_dir('apps/utility/fluidr3_gm2-2.sf2')
)
MIDISHOP_ENVIRONMENT = env('MIDISHOP_ENVIRONMENT', default='development')

# Email
# -----------------------------------------------------------------------------
CONTACT_EMAIL = env('CONTACT_EMAIL', default=None)
SERVER_EMAIL = env('SERVER_EMAIL', default='noreply@mail.midisonline.com')
EMAIL_BACKEND = env('EMAIL_BACKEND', default=None)
EMAIL_HOST = env('EMAIL_HOST', default=None)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default=None)
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default=None)
EMAIL_PORT = env.int('EMAIL_PORT', default=25)

if EMAIL_PORT:
    EMAIL_USE_TLS = True

# Oscar Settings
# -----------------------------------------------------------------------------
OSCAR_SHOP_NAME = SITE_NAME
OSCAR_SHOP_TAGLINE = ''
OSCAR_FROM_EMAIL = SERVER_EMAIL
OSCAR_DEFAULT_CURRENCY = 'USD'
OSCAR_ALLOW_ANON_CHECKOUT = True
OSCAR_GOOGLE_ANALYTICS_ID = env('OSCAR_GOOGLE_ANALYTICS_ID', default=None)

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
    }
]

OSCAR_SEARCH_FACETS = {
    'fields': OrderedDict([
        ('product_class', {'name': _('Type'), 'field': 'product_class'}),
        # categories are already shown by default
        # ('category', {'name': _('Type'), 'field': 'category'}),
        ('rating', {'name': _('Rating'), 'field': 'rating'}),
        ('genre', {'name': _('Genre'), 'field': 'genre'}),
        ('artist', {'name': _('Artist'), 'field': 'artist'}),
    ]),
    'queries': OrderedDict([
        ('price_range', {
            'name': _('Price range'),
            'field': 'price',
            'queries': [
                # This is a list of (name, query) tuples where the name will
                # be displayed on the front-end.
                (_('0 to 5'), '[0 TO 5]'),
                (_('5 to 20'), '[5 TO 20]'),
                (_('20 to 40'), '[20 TO 40]'),
                (_('40+'), '[40 TO *]'),
            ]
        }),
        ('rating', {
            'name': _('Rating'),
            'field': 'rating',
            'queries': [
                # This is a list of (name, query) tuples where the name will
                # be displayed on the front-end.
                (_('5 stars'), '5'),
                (_('4 stars'), '4'),
                (_('3 stars'), '3'),
                (_('2 stars'), '2'),
                (_('1 star'), '1'),
            ]
        }),
    ]),
}
OSCAR_MISSING_IMAGE_URL = append_to_base_dir('pianosite/public/media/placeholder.png')

LANGUAGES = (
    ('en-us', _('English')),
    ('es', _('Español')),
)

# DJ-STRIPE
STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
STRIPE_API_VERSION = env('STRIPE_API_VERSION', default='2012-11-07')

# Sentry
# ------------------------------------------------------------------------------
SENTRY_DSN = env('SENTRY_DSN', default=None)
if SENTRY_DSN:
    INSTALLED_APPS += ['raven.contrib.django.raven_compat']
    RAVEN_CONFIG = {
        'dsn': SENTRY_DSN,
        'environment': MIDISHOP_ENVIRONMENT,
        'release': __version__,
    }


# Django Debug Toolbar
# ------------------------------------------------------------------------------
DEBUG_TOOLBAR = env.bool('DEBUG_TOOLBAR', default=DEBUG)
if DEBUG_TOOLBAR:
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': env.bool('TOOLBAR_INTERCEPT', default=False)
    }
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# Default logging for Django. This sends an email to the site admins on every
# HTTP 500 error. Depending on DEBUG, all other log records are either sent to
# the console (DEBUG=True) or discarded by mean of the NullHandler (DEBUG=False)
# See http://docs.djangoproject.com/en/dev/topics/logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s:%(asctime)s: %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': False,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins', 'console', 'sentry'],
            'level': 'ERROR',
            'propagate': False,
        },
        'celery': {
            'level': 'INFO',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        'celery.task': {
            'level': 'INFO',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        'gunicorn': {
            'level': 'INFO',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        'apps': {
            'level': 'INFO',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        'pianosite': {
            'level': 'INFO',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        'raven': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
        # Catch All Logger -- Captures any other logging
        '': {
            'handlers': ['console', 'sentry', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
