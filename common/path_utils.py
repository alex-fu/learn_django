# coding=utf-8

import os
import shutil

from common import error


def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    elif os.path.isdir(directory_path):
        return
    else:
        raise error.ServerException('path[{}] exists and is not directory'.format(directory_path))


def clean_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    elif os.path.isdir(directory_path):
        for path in os.listdir(directory_path):
            remove_path(os.path.join(directory_path, path))
    else:
        raise error.ServerException('path[{}] is not directory'.format(directory_path))


def remove_path(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)
        else:
            raise error.ServerException('nonsupport type for remove path[{}]'.format(path))
    else:
        return


if __name__ == '__main__':
    TMP_DIR = '/workspace/learn_django/tmp'
    create_directory(TMP_DIR)
    clean_directory(TMP_DIR)
