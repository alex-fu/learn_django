# coding=utf-8

import logging
import requests
import re
from html.parser import HTMLParser

from common import error
import common as utils

logger = logging.getLogger('crawler')

__all__ = [
    'get_changed_stock_list'
]


class ReportParser(HTMLParser):
    def __init__(self):
        super(ReportParser, self).__init__()
        self.flag = None
        self.codes = []
        self.count = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'td' and ('class', 'dm') in attrs:
            self.flag = 'dm'
        if tag == 'span' and ('class', 'count') in attrs:
            self.flag = 'count'

    def handle_endtag(self, tag):
        self.flag = None

    def handle_data(self, data):
        if self.flag == 'dm':
            self.codes.append(data.strip())
        if self.flag == 'count':
            m = re.match('共.*?(\d+)条', data.strip())
            if m is not None:
                self.count = int(m.group(1))


def _get_latest_report_html(report_type, page_no, start_time=None, end_time=None):
    to_notice_type = {1: '010305', 2: '010303', 3: '010307', 4: '010301'}
    cur_dt = utils.current_datetime()
    today = '%d-%02d-%02d' % (cur_dt.year, cur_dt.month, cur_dt.day)
    url = 'http://www.cninfo.com.cn/search/search.jsp'
    data = {'orderby': 'date11', 'marketType': '', 'stockCode': '', 'keyword': '',
            'noticeType': to_notice_type[report_type], 'pageNo': page_no,
            'startTime': today if start_time is None else start_time,
            'endTime': today if end_time is None else end_time}
    resp = requests.post(url, data)
    if resp is not None and resp.ok:
        return resp.content.decode('gbk')
    else:
        raise error.ServerException(error.SERVER_ERR_DOWNLOAD_FAILED, 'download html from {} failed'.format(url))


def _get_latest_report_list(report_type, page_no, start_time=None, end_time=None):
    parser = ReportParser()
    parser.feed(_get_latest_report_html(report_type, page_no, start_time, end_time))
    return list(parser.codes), parser.count


def get_latest_report_list(report_type, start_time=None, end_time=None):
    code_list, total_count = _get_latest_report_list(report_type, 1, start_time, end_time)

    page_no = 2
    while len(code_list) < total_count and page_no < total_count:
        _code_list, _ = _get_latest_report_list(report_type, page_no, start_time, end_time)
        if len(_code_list) == 0:
            break
        code_list.extend(_code_list)
        page_no += 1
    return code_list


def get_changed_stock_list(start_time=None, end_time=None):
    changed_codes = []
    for report_type in (1, 2, 3, 4):
        changed_codes.extend(get_latest_report_list(report_type, start_time, end_time))
    return list(set(changed_codes))


if __name__ == '__main__':
    print(get_latest_report_list(1))
    print(get_latest_report_list(2))
    print(get_latest_report_list(3))
    print(get_latest_report_list(4))
