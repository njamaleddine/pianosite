import logging

from django.conf import settings
from django.core.exceptions import DisallowedHost

from raven import Client


logger = logging.getLogger(__name__)

HTTP_META_FOR_SENTRY = ('HTTP_USER_AGENT', 'PATH_INFO', 'REMOTE_ADDR', 'REMOTE_HOST')


class GroupDisallowedHostExceptionMiddleware(object):
    """
    If using Sentry (raven) then add fingerprint to Disallowed Host
    exceptions so Sentry can group them
    """
    def process_response(self, request, response):
        meta_from_request = {
            k: v for k, v in request.META.items() if k in HTTP_META_FOR_SENTRY
        }

        if hasattr(settings, 'RAVEN_CONFIG'):
            try:
                request.get_host()
            except DisallowedHost:
                client = Client(**settings.RAVEN_CONFIG)
                client.extra_context(meta_from_request)
                client.captureException(
                    fingerprint=['django.security.DisallowedHost'],
                    tags={'http_host': request.META.get('HTTP_HOST', '')},
                )
                logger.info('ALLOWED_HOST Error', extra=meta_from_request)
        else:
            request.get_host()

        return response
