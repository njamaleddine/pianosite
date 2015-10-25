"""
Django settings for pianosite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
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


# Project specific information
SITE_NAME = u"Piano Site"
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
] + get_core_apps([
    'apps.catalogue',
    'apps.checkout',
    'apps.dashboard',
    'apps.dashboard.catalogue',
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
    location('static/'),
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
SERVER_EMAIL = "django@localhost"
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

# Oscar Paypal
OSCAR_DASHBOARD_NAVIGATION.append(
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
)

# Oscar Paypal Support
PAYPAL_API_USERNAME = os.environ.get("PAYPAL_API_USERNAME", "")
PAYPAL_API_PASSWORD = os.environ.get("PAYPAL_API_PASSWORD", "")
PAYPAL_API_SIGNATURE = os.environ.get("PAYPAL_API_SIGNATURE", "")
# Taken from PayPal's documentation - these should always work in the sandbox
PAYPAL_SANDBOX_MODE = coerce_bool(os.environ.get("PAYPAL_API_USERNAME", True))
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
    ('es', _('Spanish')),
)
