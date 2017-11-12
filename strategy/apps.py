# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

import logging

logger = logging.getLogger('strategy')


class StrategyConfig(AppConfig):
    name = 'strategy'

    def ready(self):
        logger.info('strategy is ready')
