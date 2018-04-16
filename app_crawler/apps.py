import logging

from django.apps import AppConfig

logger = logging.getLogger('download')


class DownloadConfig(AppConfig):
    name = 'download'

    def ready(self):
        logger.info('download is ready')
