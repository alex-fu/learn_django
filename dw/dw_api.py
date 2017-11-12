# coding=utf-8
import os

import pandas as pd
from utils import FINANCE_SHEET_DIR


def _parse_csv(csv_name, encoding, index_column_index):
    df = pd.read_csv(csv_name, encoding=encoding, index_col=index_column_index)
    return df


def _get_base_path():
    return FINANCE_SHEET_DIR


def _get_finance_filename(stock_code, sheet_type, term_type):
    csv_name = "{}_{}_{}.csv".format(sheet_type, term_type, stock_code)
    return os.path.join(_get_base_path(), stock_code, csv_name)


def parse_finance_file(stock_code, sheet_type, term_type):
    csv_name = _get_finance_filename(stock_code, sheet_type, term_type)
    return _parse_csv(csv_name, "gbk", 0)


def _do_example():
    df = parse_finance_file("603998", "lrb", "report")
    # print(df)
    # print(df.ix[u"营业总收入(万元)"])
    print(df["2017-09-30"][u"营业总收入(万元)"])

if __name__ == "__main__":
    _do_example()
