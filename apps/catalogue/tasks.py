import logging

from django.core.management import call_command

from celery import shared_task


logger = logging.getLogger(__name__)


@shared_task
def update_search_index():
    """ Update haystack search index """
    logger.info('Updating haystack search index')
    call_command('update_index', interactive=False)


@shared_task
def rebuild_search_index():
    """ Rebuild haystack search index """
    logger.info('Rebuilding haystack search index')
    call_command('rebuild_index', interactive=False)
