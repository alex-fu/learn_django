# coding=utf-8

import logging

import numpy as np
import tushare as ts

from common.constant import *
from common import error
import common as utils

logger = logging.getLogger('crawler')

__all__ = [
    'download_stock_basics',
    'get_stock_basics_csv',
    'get_stock_basics_df',
    'get_stock_list'
]


_stock_basics_file_path = os.path.join(BASIC_DIR, 'stock_basics.csv')


def download_stock_basics():
    utils.clean_directory(BASIC_DIR)
    try:
        df = ts.get_stock_basics()
        utils.df2csv(df, _stock_basics_file_path)
    except Exception as e:
        logger.error('download_categories failed. {}'.format(error.exception_string(e)))
        utils.clean_directory(BASIC_DIR)
        raise error.ServerException(error.SERVER_ERR_DOWNLOAD_FAILED, error.exception_string(e))


def get_stock_basics_csv(force=False):
    if force or not os.path.exists(_stock_basics_file_path):
        download_stock_basics()
    return _stock_basics_file_path


def get_stock_basics_df(force=False):
    return utils.csv2df(get_stock_basics_csv(force), dtype={'code': np.str_})


def get_stock_list(force=False):
    return [code for code in utils.df_get_row_index_list(get_stock_basics_df(force))]


if __name__ == '__main__':
    codes = get_stock_list()
    print(len(codes))
    print(codes)
