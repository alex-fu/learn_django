# coding=utf-8

import os
import json
import requests
import codecs
import time
from xid import Xid
import threading

from . import error
from . import path_utils


_model_request_lock = threading.Lock()


def model_request(func, *args):
    with _model_request_lock:
        return func(*args)


def get_uuid():
    return Xid().string()


def json_file_to_dict(file_path):
    with open(file_path, 'rb') as f:
        return json.load(f, encoding='utf-8')
