# coding=utf-8

import threading


class SingletonType(type):
    def __init__(cls, what, bases=None, attr_dict=None):
        cls._instance_lock = threading.Lock()
        super(SingletonType, cls).__init__(what, bases, attr_dict)

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance
