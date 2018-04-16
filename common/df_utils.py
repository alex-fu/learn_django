# coding=utf-8

import pandas as pd
import numpy as np
from decimal import Decimal

from . import error


def series_list_to_df_as_row(row_series_list):
    return pd.DataFrame(row_series_list, columns=row_series_list[0].index)


def series_list_to_df_as_col(col_series_list):
    return pd.concat(col_series_list, axis=1)


def df2csv(df, csv_path):
    df.to_csv(csv_path, encoding='utf-8')


def csv2df(csv_path, index_col=0, dtype=None):
    try:
        if dtype is None:
            if index_col is None:
                df = pd.read_csv(csv_path, encoding='utf-8')
            else:
                df = pd.read_csv(csv_path, encoding='utf-8', index_col=index_col)
        else:
            df = pd.read_csv(csv_path, encoding='utf-8', dtype=dtype)
            if index_col is not None:
                df.set_index(df.columns[index_col], inplace=True)
        return df
    except Exception as e:
        raise error.ServerException(error.SERVER_ERR_INTERNAL,
                                    'wrong csv[{}].{}'.format(csv_path, error.exception_string(e)))


def df_numeric_is_nan(value):
    return np.isnan(value)


def df_numeric_to_string(value, precision=2):
    precision_decimal = Decimal('0.' + ''.join(map(lambda i: '0', range(0, precision))))
    return Decimal('{}'.format(value)).quantize(precision_decimal).to_eng_string()


def df_numeric_deviation(value1, value2, deviation):
    diff = value1 - value2
    return deviation > diff > deviation * (-1)


def df_get_row_index_list(df):
    return list(df.index.get_values())


def df_get_col_index_list(df):
    return list(df.columns.get_values())


def df_get_row(df, row_name, raise_e=True):
    if not isinstance(df, pd.DataFrame):
        raise error.ServerException(error.SERVER_ERR_INTERNAL, 'wrong type(df): {}'.format(type(df)))
    if row_name in df.index:
        return df.ix[row_name]
    elif not raise_e:
        return pd.Series(index=df.columns, name=row_name, data='--')
    else:
        raise error.ServerException(error.SERVER_ERR_INTERNAL, 'get wrong row[{}] not in [{}]'.format(row_name, df.index))


def df_get_col(df, col_name, raise_e=True):
    if not isinstance(df, pd.DataFrame):
        raise error.ServerException(error.SERVER_ERR_INTERNAL, 'wrong type(df): {}'.format(type(df)))
    if col_name in df.columns:
        return df[col_name]
    elif not raise_e:
        return pd.Series(index=df.index, name=col_name, data='--')
    else:
        raise error.ServerException(error.SERVER_ERR_INTERNAL, 'get wrong col[{}] not in [{}]'.format(col_name, df.columns))


def df_get_rows(df, row_name_list, raise_e=True):
    if not isinstance(df, pd.DataFrame):
        raise error.ServerException(error.SERVER_ERR_INTERNAL, 'wrong type(df): {}'.format(type(df)))
    row_series_list = [df_get_row(df, row_name, raise_e) for row_name in row_name_list]
    new_df = series_list_to_df_as_row(row_series_list)
    return new_df


def df_get_cols(df, col_name_list, raise_e=True):
    if not isinstance(df, pd.DataFrame):
        raise error.ServerException(error.SERVER_ERR_INTERNAL, 'wrong type(df): {}'.format(type(df)))
    col_series_list = [df_get_col(df, col_name, raise_e) for col_name in col_name_list]
    new_df = series_list_to_df_as_col(col_series_list)
    return new_df


def df_get_row_numeric(df, row_name, raise_e=True):
    return pd.to_numeric(df_get_row(df, row_name, raise_e), errors='coerce', downcast='float')


def df_get_col_numeric(df, col_name, raise_e=True):
    return pd.to_numeric(df_get_col(df, col_name, raise_e), errors='coerce', downcast='float')


def df_concat(df_list, df_name_list=None):
    if df_name_list is not None:
        return pd.concat(df_list, keys=df_name_list)
    else:
        return pd.concat(df_list)
