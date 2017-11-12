# coding=utf-8

"""
reference documents/finance_url.txt
"""
import os
import time
from utils import create_path, download_file, DOWNLOADS_DIR


def download_all_financial_data(stock_code):
    base_path = os.path.join(DOWNLOADS_DIR, 'finance', stock_code)
    create_path(base_path)

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

    def _download_url(_sheet_type, _term_type, _sheet_part):
        base_url = 'http://quotes.money.163.com/service/{}_{}.html?type={}'.format(_sheet_type, stock_code, _term_type)
        if _sheet_part != '':
            return '{}&part={}'.format(base_url, _sheet_part)
        return base_url

    def _download_file_path(_sheet_type, _term_type, _sheet_part):
        if _sheet_part == '':
            return os.path.join(base_path, '{}_{}_{}.csv'.format(_sheet_type, _term_type, stock_code))
        else:
            return os.path.join(base_path, '{}_{}_{}_{}.csv'.format(_sheet_type, _sheet_part, _term_type, stock_code))

    for sheet_type, sheet_info in sheet_types.items():
        for sheet_part in sheet_info['parts']:
            for term_type in sheet_info['terms']:
                download_file(_download_url(sheet_type, term_type, sheet_part),
                              _download_file_path(sheet_type, term_type, sheet_part))
                time.sleep(1)


if __name__ == "__main__":
    download_all_financial_data('300438')
