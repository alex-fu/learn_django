# coding=utf-8

import logging

import numpy as np
import tushare as ts

from common.constant import *
from common import error
import common as utils

logger = logging.getLogger('crawler')

__all__ = [
    'download_forecast',
    'get_forecast_csv',
    'get_forecast_df'
]


def _forecast_file_path(year, quarter):
    return os.path.join(FORECAST_DIR, "forecast_{}_{}.csv".format(year, quarter))


def download_forecast(year, quarter):
    try:
        df = ts.forecast_data(year, quarter)
        df.set_index('code', inplace=True)
        utils.df2csv(df, _forecast_file_path(year, quarter))
    except Exception as e:
        logger.error('download_forecast(year[{}], quarter[{}]) failed.{}'.format(
            year, quarter, error.exception_string(e)))
        raise error.ServerException(error.SERVER_ERR_DOWNLOAD_FAILED, error.exception_string(e))


def get_forecast_csv(year, quarter, force=False):
    file_path = _forecast_file_path(year, quarter)
    if force or not os.path.exists(file_path):
        download_forecast(year, quarter)
    return file_path


def get_forecast_df(year, quarter, force=False):
    return utils.csv2df(get_forecast_csv(year, quarter, force), dtype={'code': np.str_})


if __name__ == "__main__":
    download_forecast(2017, 4)
    print(get_forecast_df(2017, 4))
