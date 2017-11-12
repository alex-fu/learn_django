import logging

from jsonrpc import jsonrpc_method

logger = logging.getLogger('strategy')


@jsonrpc_method('strategy.test')
def test(request):
    logger.log('test')
    return


@jsonrpc_method('strategy.rpc_download_finance_sheet')
def rpc_download_finance_sheet(request, arg_dict):
    from dw import download_finance_sheet

    stock_code = arg_dict['stock_code']
    download_finance_sheet.download_all_financial_data(stock_code)
