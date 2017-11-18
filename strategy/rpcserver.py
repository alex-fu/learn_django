import logging
from jsonrpc import jsonrpc_method

from error import *
import rpchandler

logger = logging.getLogger('strategy')


def raise_exception(request, e, content=None):
    from jsonrpc.exceptions import ServerError
    import traceback

    is_rds_exception = isinstance(e, ServerException)
    if is_rds_exception:
        err_msg = 'rds error code: {}, msg: {}'.format(e.err_code, e.err_msg)
    else:
        err_msg = '{}\n{}'.format(e, traceback.format_exc())

    if content is not None:
        logger.error('{} failed. {}'.format(content, err_msg))

    if request is not None:
        raise ServerError(err_msg)
    elif is_rds_exception:
        raise e
    else:
        raise ServerException(SERVER_ERR_INTERNAL, err_msg)


@jsonrpc_method('strategy.test')
def test(request):
    content = 'request test()'
    logger.info(content)
    try:
        ret = 'Hello World!'
    except Exception, e:
        raise_exception(request, e, content)
    else:
        logger.info('{} successfully.'.format(content))
        return ret


@jsonrpc_method('strategy.rpc_download_finance_sheet')
def rpc_download_finance_sheet(request, arg_dict):
    content = 'request rpc_download_finance_sheet(arg_dict[{}])'.format(arg_dict)
    logger.info(content)
    try:
        ret = rpchandler.rpc_download_finance_sheet(arg_dict)
    except Exception, e:
        raise_exception(request, e, content)
    else:
        logger.info('{} successfully.'.format(content))
        return ret


@jsonrpc_method('strategy.rpc_lijie_basic')
def rpc_lijie_basic(request, arg_dict):
    content = 'request rpc_lijie_basic(arg_dict[{}])'.format(arg_dict)
    logger.info(content)
    try:
        ret = rpchandler.rpc_lijie_basic(arg_dict)
    except Exception, e:
        raise_exception(request, e, content)
    else:
        logger.info('{} successfully.'.format(content))
        return ret


@jsonrpc_method('strategy.rpc_financial_get_data')
def rpc_financial_get_data(request, arg_dict):
    content = 'request rpc_financial_get_data(arg_dict[{}])'.format(arg_dict)
    logger.info(content)
    try:
        ret = rpchandler.rpc_financial_get_data(arg_dict)
    except Exception, e:
        raise_exception(request, e, content)
    else:
        logger.info('{} successfully.'.format(content))
        return ret


@jsonrpc_method('strategy.rpc_financial_indicator_import')
def rpc_financial_indicator_import(request):
    content = 'request rpc_financial_indicator_import()'
    logger.info(content)
    try:
        ret = rpchandler.rpc_financial_indicator_import()
    except Exception, e:
        raise_exception(request, e, content)
    else:
        logger.info('{} successfully.'.format(content))
        return ret


@jsonrpc_method('strategy.rpc_financial_strategy_add')
def rpc_financial_strategy_add(request, strategy_name, indicator_list):
    content = 'request rpc_financial_strategy_add(strategy_name[{}], indicator_list[{}])'.\
        format(strategy_name, indicator_list)
    logger.info(content)
    try:
        ret = rpchandler.rpc_financial_strategy_add(strategy_name, indicator_list)
    except Exception, e:
        raise_exception(request, e, content)
    else:
        logger.info('{} successfully.'.format(content))
        return ret


@jsonrpc_method('strategy.rpc_financial_strategy_update')
def rpc_financial_strategy_update(request, strategy_id, indicator_list):
    content = 'request rpc_financial_strategy_update(strategy_id[{}], indicator_list[{}])'\
        .format(strategy_id, indicator_list)
    logger.info(content)
    try:
        ret = rpchandler.rpc_financial_strategy_update(strategy_id, indicator_list)
    except Exception, e:
        raise_exception(request, e, content)
    else:
        logger.info('{} successfully.'.format(content))
        return ret


@jsonrpc_method('strategy.rpc_financial_strategy_copy')
def rpc_financial_strategy_copy(request, strategy_name, old_strategy_id):
    content = 'request rpc_financial_strategy_copy(strategy_name[{}], old_strategy_id[{}])'\
        .format(strategy_name, old_strategy_id)
    logger.info(content)
    try:
        ret = rpchandler.rpc_financial_strategy_copy(strategy_name, old_strategy_id)
    except Exception, e:
        raise_exception(request, e, content)
    else:
        logger.info('{} successfully.'.format(content))
        return ret
