# -*- coding: utf-8 -*-

import logging
from jsonrpc import jsonrpc_method

from common.error import *
from . import rpchandler

logger = logging.getLogger('strategy')


def raise_exception(request, e, content=None):
    from jsonrpc.exceptions import ServerError
    import traceback

    if isinstance(e, ServerException):
        raise_e = e
    else:
        raise_e = ServerException(SERVER_ERR_INTERNAL, '{}\n{}'.format(e, traceback.format_exc()))

    err_msg = 'server error code: {}, msg: {}'.format(raise_e.err_code, raise_e.err_msg)
    # log err
    if content is not None:
        logger.error('{} failed. {}'.format(content, err_msg))
    # raise exception
    if request is not None:
        raise ServerError(err_msg)
    else:
        raise raise_e


def operation_exec(request, func, **kwargs):
    try:
        ret = func(**kwargs)
    except Exception as e:
        raise_exception(request, e)
    else:
        return ret


def operation_exec_and_log(request, func, **kwargs):
    content = 'request {}({})'.format(getattr(func, '__name__'), kwargs)
    logger.info(content)
    try:
        ret = func(**kwargs)
    except Exception as e:
        raise_exception(request, e, content)
    else:
        logger.info('{} successfully.'.format(content))
        return ret


@jsonrpc_method('strategy.test')
def test(request):
    content = 'request test()'
    logger.info(content)
    try:
        ret = 'Hello World!'
    except Exception as e:
        raise_exception(request, e, content)
    else:
        logger.info('{} successfully.'.format(content))
        return ret


@jsonrpc_method('strategy.rpc_download_finance_sheet')
def rpc_download_finance_sheet(request, arg_dict):
    return operation_exec_and_log(request, rpchandler.rpc_download_finance_sheet, arg_dict=arg_dict)


@jsonrpc_method('strategy.rpc_lijie_basic')
def rpc_lijie_basic(request, arg_dict):
    return operation_exec_and_log(request, rpchandler.rpc_lijie_basic, arg_dict=arg_dict)


@jsonrpc_method('strategy.rpc_financial_get_data')
def rpc_financial_get_data(request, arg_dict):
    return operation_exec_and_log(request, rpchandler.rpc_financial_get_data, arg_dict=arg_dict)


@jsonrpc_method('strategy.rpc_financial_indicator_import')
def rpc_financial_indicator_import(request):
    return operation_exec_and_log(request, rpchandler.rpc_financial_indicator_import)


@jsonrpc_method('strategy.rpc_financial_strategy_add')
def rpc_financial_strategy_add(request, strategy_name, indicator_list):
    return operation_exec_and_log(request, rpchandler.rpc_financial_strategy_add,
                                  strategy_name=strategy_name, indicator_list=indicator_list)


@jsonrpc_method('strategy.rpc_financial_strategy_update')
def rpc_financial_strategy_update(request, strategy_id, indicator_list):
    return operation_exec_and_log(request, rpchandler.rpc_financial_strategy_update,
                                  strategy_id=strategy_id, indicator_list=indicator_list)


@jsonrpc_method('strategy.rpc_financial_strategy_copy')
def rpc_financial_strategy_copy(request, strategy_name, old_strategy_id):
    return operation_exec_and_log(request, rpchandler.rpc_financial_strategy_copy,
                                  strategy_name=strategy_name, old_strategy_id=old_strategy_id)


@jsonrpc_method('strategy.rpc_financial_strategy_delete')
def rpc_financial_strategy_delete(request, strategy_id):
    return operation_exec_and_log(request, rpchandler.rpc_financial_strategy_delete, strategy_id=strategy_id)
