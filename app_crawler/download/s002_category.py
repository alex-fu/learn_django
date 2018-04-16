# coding=utf-8

import logging
import numpy as np
import tushare as ts

from common.constant import *
from common import error
import common as utils

logger = logging.getLogger('crawler')

__all__ = [
    'download_categories',
    'get_category_csv',
    'get_category_df'
]

_all_categories = {
    'industry': ('get_industry_classified',),
    'concept': ('get_concept_classified',),
    'area': ('get_area_classified',),
    'sme': ('get_sme_classified',),
    'gem': ('get_gem_classified',),
    'st': ('get_st_classified',),
    'hs300': ('get_hs300s',),
    'sz50': ('get_sz50s',),
    'zz500': ('get_zz500s',),
    'terminated': ('get_terminated',),
    'suspended': ('get_suspended',),
}


def _category_file_path(category_method):
    return os.path.join(CATEGORY_DIR, 'category_{}.csv'.format(category_method))


def download_categories():
    utils.clean_directory(CATEGORY_DIR)
    try:
        for category_method, (func_name,) in _all_categories.items():
            try:
                df = getattr(ts, func_name)()
                df.set_index('code', inplace=True)
                utils.df2csv(df, _category_file_path(category_method))
            except Exception as e:
                logger.error('download_categories[{}] failed. {}'.format(category_method, error.exception_string(e)))
                raise e
    except Exception as e:
        utils.clean_directory(CATEGORY_DIR)
        raise error.ServerException(error.SERVER_ERR_DOWNLOAD_FAILED, error.exception_string(e))


def get_category_csv(category_method, force=False):
    file_path = _category_file_path(category_method)
    if force or not os.path.exists(file_path):
        download_categories()
    return file_path


def get_category_df(category_method, force=False):
    return utils.csv2df(get_category_csv(category_method, force), dtype={'code': np.str_})


if __name__ == "__main__":
    download_categories()
