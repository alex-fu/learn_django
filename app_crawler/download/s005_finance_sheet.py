# coding=utf-8

"""
reference documents/finance_url.txt
"""
import logging
import requests
import codecs

from common.constant import *
from common import error
import common as utils

logger = logging.getLogger('crawler')

__all__ = [
    'download_all_financial_data',
    'downloaded_newest_report_time',
    'get_finance_sheet'
]

sheet_types = {
    # 主要财务指标
    # ylnl -- 盈利能力, chnl -- 偿还能力, cznl -- 成长能力, yynl -- 营运能力
    'zycwzb': {'terms': ['report', 'year', 'season'], 'parts': ['', 'ylnl', 'chnl', 'cznl', 'yynl']},
    # 财务报表摘要
    'cwbbzy': {'terms': ['report', 'year'], 'parts': ['']},
    # 资产负债表
    'zcfzb': {'terms': ['report', 'year'], 'parts': ['']},
    # 利润表
    'lrb': {'terms': ['report', 'year'], 'parts': ['']},
    # 现金流量表
    'xjllb': {'terms': ['report', 'year'], 'parts': ['']},
}


def finance_sheet_directory(stock_code):
    return os.path.join(FINANCE_DIR, stock_code)


def finance_sheet_file_path(stock_code, sheet_type, term_type, sheet_part):
    # check param
    if sheet_type not in sheet_types or term_type not in sheet_types[sheet_type]['terms'] or \
                    sheet_part not in sheet_types[sheet_type]['parts']:
        raise error.ServerException(
            error.SERVER_ERR_INTERNAL,
            'wrong param: stock_code[{}], sheet_type[{}], term_type[{}], sheet_part[{}]'.format(
                stock_code, sheet_type, term_type, sheet_part)
        )

    sheet_directory = finance_sheet_directory(stock_code)
    if sheet_part == '':
        return os.path.join(sheet_directory, '{}_{}_{}.csv'.format(sheet_type, term_type, stock_code))
    else:
        return os.path.join(sheet_directory, '{}_{}_{}_{}.csv'.format(sheet_type, sheet_part, term_type, stock_code))


def _download_url(stock_code, sheet_type, term_type, sheet_part):
    base_url = 'http://quotes.money.163.com/service/{}_{}.html?type={}'.format(sheet_type, stock_code, term_type)
    if sheet_part != '':
        return '{}&part={}'.format(base_url, sheet_part)
    return base_url


def _download_sheet(stock_code, sheet_type, term_type, sheet_part):
    detail = 'download finance_sheet(sheet_type[{}], term_type[{}], sheet_part[{}]) failed.'.format(
        sheet_type, term_type, sheet_part)
    try:
        resp = requests.get(_download_url(stock_code, sheet_type, term_type, sheet_part), stream=True)
        if resp is not None and resp.ok:
            lines = [line.strip() for line in resp.content.decode('gbk').replace('\r\n', '\n').strip().split('\n')]
            lines = [line if line[-1] != ',' else line[0:-1] for line in lines if line != '']
            lines.append('')
            with codecs.open(finance_sheet_file_path(stock_code, sheet_type, term_type, sheet_part), 'w', 'utf-8') as f:
                f.write('\n'.join(lines))
        else:
            raise error.ServerException(error.SERVER_ERR_DOWNLOAD_FAILED, detail)
    except error.ServerException as e:
        logger.error('{}.'.format(detail))
        raise e
    except Exception as e:
        raise error.ServerException(error.SERVER_ERR_DOWNLOAD_FAILED, '{}.{}'.format(detail, error.exception_string(e)))


def download_all_financial_sheet(stock_code):
    utils.clean_directory(finance_sheet_directory(stock_code))
    try:
        for sheet_type, sheet_info in sheet_types.items():
            for sheet_part in sheet_info['parts']:
                for term_type in sheet_info['terms']:
                    _download_sheet(stock_code, sheet_type, term_type, sheet_part)
        utils.sleep(1)
    except Exception as e:
        logger.error('download_all_financial_sheet(stock_code[{}]) failed.{}'.format(
            stock_code, error.exception_string(e)))
        utils.clean_directory(finance_sheet_directory(stock_code))
        raise e


def get_finance_sheet_csv(stock_code, sheet_type, term_type, sheet_part='', force=False):
    file_path = finance_sheet_file_path(stock_code, sheet_type, term_type, sheet_part)
    if force or not os.path.exists(file_path):
        download_all_financial_sheet(stock_code)
    return file_path


def get_finance_sheet_df(stock_code, sheet_type, term_type, sheet_part='', force=False):
    return utils.csv2df(get_finance_sheet_csv(stock_code, sheet_type, term_type, sheet_part, force))


def downloaded_newest_report_time(stock_code):
    file_path = finance_sheet_file_path(stock_code, 'lrb', 'report', '')
    return utils.df_get_col_index_list(utils.csv2df(file_path))[0]


if __name__ == "__main__":
    # print(_download_sheet('300438', 'lrb', 'report', ''))
    download_all_financial_sheet('300438')
    print(get_finance_sheet_df('300438', 'lrb', 'report'))
    print(downloaded_newest_report_time('300438'))
