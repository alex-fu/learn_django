# coding=utf-8

from utils import *


def get_finance_sheet(stock_code, sheet_type, term_type, sheet_part='', force_download=False):
    import download_finance_sheet
    file_path = download_finance_sheet.finance_sheet_file_path(stock_code, sheet_type, term_type, sheet_part)
    if force_download or not os.path.exists(file_path):
        download_finance_sheet.download_all_financial_data(stock_code)

    return csv2df(file_path)


if __name__ == "__main__":
    df = get_finance_sheet('603998', 'lrb', 'report')
    print(df['2017-09-30'][u'营业总收入(万元)'])
