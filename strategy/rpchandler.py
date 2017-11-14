import logging

from error import *
from financial_indicator import FinanceIndicator

logger = logging.getLogger('strategy')


def rpc_download_finance_sheet(arg_dict):
    from dw import download_finance_sheet

    code = arg_dict['code']
    download_finance_sheet.download_all_financial_data(code)


def rpc_lijie_basic(arg_dict):
    try:
        code = arg_dict['code']
        date_list = arg_dict['date_list']
    except Exception, e:
        raise ServerException(SERVER_ERR_WRONG_PARAM, exception_string(e))

    fi = FinanceIndicator(code, date_list)
    print fi.gross_profit_rate()



