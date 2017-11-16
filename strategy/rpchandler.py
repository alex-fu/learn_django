import logging

from utils import *
from financial_indicator import FinanceIndicator

logger = logging.getLogger('strategy')


def rpc_download_finance_sheet(arg_dict):
    from dw import download_finance_sheet

    code = arg_dict['code']
    download_finance_sheet.download_all_financial_data(code)


def rpc_lijie_basic(arg_dict):
    try:
        codes = arg_dict['codes'].strip()
        dates = arg_dict['dates'].strip()
    except Exception, e:
        raise ServerException(SERVER_ERR_WRONG_PARAM, exception_string(e))

    def _lijie_basic_df(fi):
        col_series_list = [fi.gross_profit_rate(), fi.net_profit_rate(), fi.three_expense_rate(),
                           fi.sales_expenses_rate(), fi.financial_expenses_rate(), fi.administrative_expenses_rate(),
                           fi.assets_liabilities_ratio(), fi.roe(), fi.total_assets_turnover_ratio(),
                           fi.cffo_net_profit_rate(), fi.major_business_income_increase_rate(),
                           fi.net_profit_exclude_increase_rate()]
        return series_list_to_df_as_row(col_series_list).transpose()

    code_list = [code.strip() for code in codes.strip().split(',') if code.strip() != '']
    date_list = [date.strip() for date in dates.strip().split(',') if date.strip() != '']
    df_list = [_lijie_basic_df(FinanceIndicator(code, date_list)) for code in code_list]
    ret_df = df_concat(df_list, code_list)
    uuid = get_uuid()
    ret_df.to_csv(os.path.join(TMP_DIR, '{}.csv'.format(uuid)), encoding='gbk')
    ret_df.to_excel(os.path.join(TMP_DIR, '{}.xls'.format(uuid)), encoding='gbk')
    return uuid, ret_df.to_html()
