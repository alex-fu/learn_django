# -*- coding: utf-8 -*-

import logging

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from common import time_utils

from dw import stock_list
from dw import finance_sheet

logger = logging.getLogger('strategy')


def meta_upsert(code, detail):
    @transaction.atomic
    def _stock_upsert():
        from .models import StockModel
        try:
            stock_o = StockModel.objects.get(code=code)
            stock_o.detail = detail
        except ObjectDoesNotExist:
            stock_o = StockModel(code, detail)
        stock_o.save()
        return stock_o

    return ModelsRequest._request(_stock_upsert)


def download_first():
    cur_dt = time_utils.current_datetime()
    codes = stock_list.get_stock_list(force=True)
    for code in codes:
        logger.info('download financial_data for stock {}'.format(code))
        finance_sheet.download_all_financial_data(code)
    # update meta
    pass


def download_update():
    pass


if __name__ == '__main__':
    download_first()
