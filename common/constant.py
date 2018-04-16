# coding=utf-8

import os

TOP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TMP_DIR = os.path.join(TOP_DIR, 'tmp')
STATIC_DIR = os.path.join(TOP_DIR, 'static')
CONFIG_DIR = os.path.join(STATIC_DIR, 'config')

DATA_DIR = os.path.join(TOP_DIR, 'data')
BASIC_DIR = os.path.join(DATA_DIR, 'basic')
CATEGORY_DIR = os.path.join(DATA_DIR, 'category')
FORECAST_DIR = os.path.join(DATA_DIR, 'forecast')
FINANCE_DIR = os.path.join(DATA_DIR, 'finance')
REPORT_DIR = os.path.join(DATA_DIR, 'report')

CRAWL_CODE_SUMMARY = 'summary'
