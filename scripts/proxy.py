# -*- coding: utf-8 -*-

import sys
import json
import re
from jsonrpc.proxy import ServiceProxy

ERR_CODE_INTERNAL = 1
ERR_CODE_WRONG_PARAMS = 2
ERR_CODE_FUNCTION_NOT_EXIST = 3
ERR_CODE_FUNCTION_WRONG_PARAMS = 4
ERR_CODE_FUNCTION_EXECUTE_FAILED = 5

RDS_ERR_RE = re.compile('ServerError: server error code: ([0-9]+), msg: (.+), details: (.+)$')


def print_csv_result(result):
    try:
        all_keys_set = set()
        for item in result:
            all_keys_set = all_keys_set | set(item.keys())
        all_keys = list(all_keys_set)
        if len(all_keys) != 0:
            print(','.join(all_keys))
            for item in result:
                print(','.join(['{}'.format(item.get(key, '')) for key in all_keys]))
    except Exception as print_e:
        print('print_csv_result failed, result: {}'.format(result))
        raise print_e


def rpc_request(app_name, func_name, args):
    content = 'function {}{}'.format(func_name, args)
    try:
        func = getattr(getattr(proxy, app_name), func_name)
        ret = func(*args)
    except Exception as exec_e:
        print('{} throw exception'.format(content))
        raise exec_e
    error_dict = ret['error']
    if error_dict is not None:
        err_code = int(error_dict.get('code', 0))
        err_message = error_dict.get('message', None)
        if err_code == -32601:
            print('{} not exist'.format(content))
            sys.exit(ERR_CODE_FUNCTION_NOT_EXIST)
        elif err_code == -32603:
            m = RDS_ERR_RE.search(err_message)
            if m is not None:
                print('server error code: {}, msg: {}, details: {}'.format(m.group(1), m.group(2), m.group(3)))
                sys.exit(ERR_CODE_FUNCTION_EXECUTE_FAILED)
            else:
                print('{} return server error, but get server error info failed. message: {}'.format(
                    content, err_message))
                sys.exit(ERR_CODE_INTERNAL)
        elif err_code == 500:
            print('{} return wrong params error, err_code: {}, err_msg: {}'.format(content, err_code, err_message))
            sys.exit(ERR_CODE_FUNCTION_WRONG_PARAMS)
        else:
            print('{} return unknown error, err_code: {}, err_msg: {}'.format(content, err_code, err_message))
            sys.exit(ERR_CODE_INTERNAL)
    else:
        result = ret['result']
        if result is None:
            sys.exit(0)
        elif isinstance(result, list) and len(list(filter(lambda r: not isinstance(r, dict), result))) == 0:
            # to csv
            print_csv_result(result)
        else:
            print(result)
        sys.exit(0)


def get_proxy():
    return ServiceProxy('http://{}:{}/json/'.format('127.0.0.1', 8000))


def usage():
    print('args: {}'.format(sys.argv))
    print('{} <app_name> <func_name> <func_args(eg:arg1,arg2)>'.format(sys.argv[0]))
    sys.exit(ERR_CODE_WRONG_PARAMS)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('nargs({}) != 4'.format(len(sys.argv)))
        usage()

    # parse args
    arg_list = None
    arg_json = None
    try:
        arg_json = '{"args": [' + sys.argv[3] + ']}'
        arg_list = json.loads(arg_json)['args']
        if not isinstance(arg_list, list):
            usage()
    except Exception as e:
        print('parse args(arg_json[{}]) failed.\n{}'.format(arg_json, e))
        usage()

    try:
        proxy = get_proxy()
        rpc_request(sys.argv[1], sys.argv[2], tuple(arg_list))
    except Exception as e:
        print(e)
        sys.exit(ERR_CODE_INTERNAL)
