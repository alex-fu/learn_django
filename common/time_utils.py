# coding=utf-8

import time
import datetime


def current_datetime():
    return datetime.datetime.now()


def current_time_string():
    return datetime_to_string(current_datetime())


def current_timestamp():
    return time.time()


def string_to_datetime(string):
    return datetime.datetime.strptime(string, "%Y%m%d_%H%M%S.%f")


def string_to_timestamp(string):
    return datetime_to_timestamp(string_to_datetime(string))


def datetime_to_string(dt):
    return dt.strftime("%Y%m%d_%H%M%S.%f")


def datetime_to_timestamp(dt):
    return time.mktime(dt.timetuple())


def diff_timestamp(ts1, ts2):
    return ts1 - ts2


def sleep(n_seconds):
    return time.sleep(n_seconds)
