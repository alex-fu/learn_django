import logging
from jsonrpc import jsonrpc_method

from common import error
from . import operations

logger = logging.getLogger('crawler')


def raise_exception(request, e, content=None):
    from jsonrpc.exceptions import ServerError
    import traceback

    if isinstance(e, error.ServerException):
        raise_e = e
    else:
        raise_e = error.ServerException(error.SERVER_ERR_INTERNAL, '{}\n{}'.format(e, traceback.format_exc()))

    err_msg = 'download error code: {}, msg: {}'.format(raise_e.err_code, raise_e.err_msg)
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


@jsonrpc_method('app_crawler.test')
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


########################################################################################################################
# operation functions
########################################################################################################################
@jsonrpc_method('app_crawler.rpc_crawl')
def rpc_crawl(request):
    return operation_exec_and_log(request, operations.crawl)


@jsonrpc_method('app_crawler.rpc_crawl_progress')
def rpc_crawl_progress(request):
    return operation_exec(request, operations.crawl_progress)
