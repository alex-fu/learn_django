import os
import requests
from xid import Xid
import time
import pandas as pd
import numpy as np
from decimal import Decimal
import codecs

from error import *

TOP_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(TOP_DIR, 'downloads')
FINANCE_SHEET_DIR = os.path.join(DOWNLOADS_DIR, 'finance')


def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def get_uuid():
    return Xid().string()


def download_csv(url, file_path, download_encoding='gbk', file_encoding='utf-8', n_tries=3):
    create_directory(os.path.dirname(file_path))

    for try_index in range(0, n_tries):
        response = requests.get(url, stream=True)
        if response is not None and response.ok:
            lines = [line.strip() for line in response.content.decode(download_encoding).split('\n')]
            # lines = [line if line[-1] != ',' else line[0:-1] for line in lines if line != '']
            lines = [line for line in lines if line != '']
            with codecs.open(file_path, 'w', file_encoding) as file_handler:
                file_handler.write('\n'.join(lines))
            return
        else:
            time.sleep(1)

    raise ServerException(SERVER_ERR_DOWNLOAD_FAILED,
                          'download from {} to file {} failed'.format(url, file_path))


def series_list_to_df_as_row(row_series_list):
    return pd.DataFrame(row_series_list, columns=row_series_list[0].index)


def series_list_to_df_as_col(col_series_list):
    return pd.concat(col_series_list, axis=1)


def csv2df(csv_path, index_col=0, encoding='utf-8'):
    try:
        df = pd.read_csv(csv_path, encoding=encoding, index_col=index_col)
        return df
    except Exception, e:
        raise ServerException(SERVER_ERR_INTERNAL,
                              'wrong csv[{}].{}'.format(csv_path, exception_string(e)))


def df_numeric_is_nan(value):
    return np.isnan(value)


def df_numeric_to_string(value, precision=2):
    precision_decimal = Decimal('0.' + ''.join(map(lambda i: '0', range(0, precision))))
    return Decimal('{}'.format(value)).quantize(precision_decimal).to_eng_string()


def df_numeric_deviation(value1, value2, deviation):
    diff = value1 - value2
    return deviation > diff > deviation * (-1)


def df_get_row(df, row_name, raise_e=True):
    if not isinstance(df, pd.DataFrame):
        raise ServerException(SERVER_ERR_INTERNAL, 'wrong type(df): {}'.format(type(df)))
    if row_name in df.index:
        return df.ix[row_name]
    elif not raise_e:
        return pd.Series(index=df.columns, name=row_name, data='--')
    else:
        raise ServerException(SERVER_ERR_INTERNAL, 'get wrong row[{}] not in [{}]'.format(row_name, df.index))


def df_get_col(df, col_name, raise_e=True):
    if not isinstance(df, pd.DataFrame):
        raise ServerException(SERVER_ERR_INTERNAL, 'wrong type(df): {}'.format(type(df)))
    if col_name in df.columns:
        return df[col_name]
    elif not raise_e:
        return pd.Series(index=df.index, name=col_name, data='--')
    else:
        raise ServerException(SERVER_ERR_INTERNAL, 'get wrong col[{}] not in [{}]'.format(col_name, df.columns))


def df_get_rows(df, row_name_list, raise_e=True):
    if not isinstance(df, pd.DataFrame):
        raise ServerException(SERVER_ERR_INTERNAL, 'wrong type(df): {}'.format(type(df)))
    row_series_list = [df_get_row(df, row_name, raise_e) for row_name in row_name_list]
    new_df = series_list_to_df_as_row(row_series_list)
    return new_df


def df_get_cols(df, col_name_list, raise_e=True):
    if not isinstance(df, pd.DataFrame):
        raise ServerException(SERVER_ERR_INTERNAL, 'wrong type(df): {}'.format(type(df)))
    col_series_list = [df_get_col(df, col_name, raise_e) for col_name in col_name_list]
    new_df = series_list_to_df_as_col(col_series_list)
    return new_df


def df_get_row_numeric(df, row_name, raise_e=True):
    return pd.to_numeric(df_get_row(df, row_name, raise_e), errors='coerce', downcast='float')


def df_get_col_numeric(df, col_name, raise_e=True):
    return pd.to_numeric(df_get_col(df, col_name, raise_e), errors='coerce', downcast='float')
