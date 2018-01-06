import logging

from django.conf import settings
from django.core.management import call_command
from celery import shared_task

from apps.utility.audio import AudioFile, MidiFile


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


@shared_task
def create_audio_samples_for_midi(product_id):
    """
    Generate audio from midi and create sample audio in mp3 and ogg format

    product (Product): instance of product
    """
    from apps.catalogue.models import Product  # no-qa, avoid circular import

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        product = None

    if product:
        with open(product.upload.path, 'rb+') as upload:
            midi = MidiFile(upload)

            with open(midi.convert_to_audio(), 'rb+') as audio_file:
                audio = AudioFile(audio_file)
                sample_ogg = audio.slice(seconds=settings.MIDISHOP_AUDIO_SAMPLE_LENGTH)

                with open(sample_ogg, 'rb+') as sample_ogg_file:
                    sample_ogg_audio = AudioFile(sample_ogg_file)
                    sample_mp3 = sample_ogg_audio.save_as_type('mp3')
                    sample_mp3_audio = AudioFile(sample_mp3)

                    product.full_audio.save(audio.name.split('/')[-1], audio, save=False)
                    product.sample_ogg.save(
                        sample_ogg_audio.name.split('/')[-1],
                        sample_ogg_audio,
                        save=False
                    )
                    product.sample_mp3.save(
                        sample_mp3_audio.name.split('/')[-1],
                        sample_mp3_audio,
                        save=False
                    )

                    product.save()


@shared_task
def create_audio_samples(product_id):
    """
    Generate audio from midi and create sample audio in mp3 and ogg format

    product (Product): instance of product
    """
    from apps.catalogue.models import Product  # no-qa, avoid circular import

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        product = None

    if product:
        with open(product.upload.path, 'rb+') as audio_file:
            audio = AudioFile(audio_file)
            sample_ogg = audio.slice(seconds=settings.MIDISHOP_AUDIO_SAMPLE_LENGTH)

            with open(sample_ogg, 'rb+') as sample_ogg_file:
                sample_ogg_audio = AudioFile(sample_ogg_file)
                sample_mp3 = sample_ogg_audio.save_as_type('mp3')
                sample_mp3_audio = AudioFile(sample_mp3)

                product.full_audio.save(audio.name.split('/')[-1], audio, save=False)
                product.sample_ogg.save(
                    sample_ogg_audio.name.split('/')[-1],
                    sample_ogg_audio,
                    save=False
                )
                product.sample_mp3.save(
                    sample_mp3_audio.name.split('/')[-1],
                    sample_mp3_audio,
                    save=False
                )

                product.save()
