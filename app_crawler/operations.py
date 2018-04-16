# -*- coding: utf-8 -*-

import logging
import threading
from django.db import transaction

from common.constant import *
from common import error
import common as utils

from .models import CrawlerModel
from . import download

logger = logging.getLogger('crawler')

_crawl_lock = threading.Lock()


class CrawlSummary(object):
    __metaclass__ = utils.SingletonType

    def __init__(self):
        try:
            summary_o = meta_get_summary_object()
        except error.ServerException:
            summary_o = None
        except Exception as e:
            raise e
        detail = {} if summary_o is None or not isinstance(summary_o.detail, dict) else summary_o.detail
        self.full_time = detail.get('full_time', None)
        self.full_complete = detail.get('full_complete', False)
        self.last_increment_time = detail.get('last_increment_time', None)
        self.increment_time = detail.get('increment_time', None)
        self.crawling = False

    def full_start(self):
        @transaction.atomic
        def _meta_start_full():
            detail = {'full_time': start_time,
                      'full_complete': False, 'last_increment_time': None, 'increment_time': None}
            summary_o = CrawlerModel(code=CRAWL_CODE_SUMMARY, detail=detail)
            summary_o.save()
            for code in codes:
                CrawlerModel(code, {}).save()

        start_time = utils.current_datetime()
        codes = download.get_stock_list(force=True)
        utils.model_request(_meta_start_full)
        with _crawl_lock:
            self.full_time = start_time

    def full_complete(self):
        @transaction.atomic
        def _meta_full_complete():
            summary_o = CrawlerModel.crawler_object(CRAWL_CODE_SUMMARY)
            summary_o.detail['full_complete'] = True
            summary_o.save()

        utils.model_request(_meta_full_complete)
        with _crawl_lock:
            self.full_complete = True

    def increment_start(self):
        @transaction.atomic
        def _meta_increment_start():
            summary_o = CrawlerModel.crawler_object(CRAWL_CODE_SUMMARY)
            summary_o.detail['increment_time'] = start_time
            summary_o.save()
            for code in codes:
                stock_o = CrawlerModel.crawler_object(code=code)
                stock_o.detail['refresh_time'] = start_time
                stock_o.save()

        start_time = utils.current_datetime()
        codes = download.get_changed_stock_list()
        utils.model_request(_meta_increment_start)
        with _crawl_lock:
            self.increment_time = start_time

    def increment_complete(self):
        @transaction.atomic
        def _meta_increment_complete():
            summary_o = CrawlerModel.crawler_object(CRAWL_CODE_SUMMARY)
            summary_o.detail['last_increment_time'] = self.increment_time
            summary_o.detail['increment_time'] = None
            summary_o.save()

        utils.model_request(_meta_increment_complete)
        with _crawl_lock:
            self.last_increment_time = self.increment_time
            self.increment_time = None


def meta_get_summary_object():
    @transaction.atomic
    def _meta_get_summary_object():
        return CrawlerModel.crawler_object(CRAWL_CODE_SUMMARY)
    return utils.model_request(_meta_get_summary_object)


def meta_get_all_stock_objects():
    @transaction.atomic
    def _meta_get_all_objects():
        return CrawlerModel.crawler_objects_all()
    return [stock_o for stock_o in utils.model_request(_meta_get_all_objects()) if stock_o.code != CRAWL_CODE_SUMMARY]


def meta_stock_download_successful(code, download_time):
    @transaction.atomic
    def _download():
        stock_o = CrawlerModel.objects.get(code=code)
        stock_o.detail['download_time'] = download_time
        stock_o.save()
    return utils.model_request(_download)


def crawl_full():
    for stock_o in meta_get_all_stock_objects():
        cur_time = utils.current_datetime()
        download.download_all_financial_sheet(stock_o.code)
        meta_stock_download_successful(stock_o.code, cur_time)


def crawl_increment():
    for stock_o in meta_get_all_stock_objects():
        if stock_o.detail['download_time'] < stock_o.detail['refresh_time']:
            cur_time = utils.current_datetime()
            download.download_all_financial_sheet(stock_o.code)
            meta_stock_download_successful(stock_o.code, cur_time)


def crawl():
    with _crawl_lock:
        if CrawlSummary().crawling:
            raise error.ServerException(error.SERVER_ERR_OP_CONCURRENT)
        else:
            CrawlSummary().crawling = True

    if CrawlSummary().full_time is None:
        CrawlSummary().full_start()

    if CrawlSummary().full_complete:
        if CrawlSummary().increment_time is None:
            CrawlSummary().increment_start()
        crawl_increment()
    else:
        crawl_full()


def crawl_progress():
    pass