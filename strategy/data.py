import logging
import json
# from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import render

from error import *
import rpcserver
from financial_indicator import FinanceIndicator
from meta import ModelsRequest

logger = logging.getLogger('strategy')


def financial_data(request):
    response = {}
    try:
        if request.method == 'POST':
            codes = request.POST.get('codes')
            dates = request.POST.get('dates')
            strategy_id = request.POST.get('strategy')
            uuid, html = rpcserver.rpc_financial_get_data(None, {'codes': codes, 'dates': dates, 'strategy_id': strategy_id})
            response['table_data'] = html
            response['uuid'] = uuid
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        else:
            all_strategies_o = ModelsRequest.financial_strategy_get_all_objects()
            all_strategies_dict = {strategy_o.id: strategy_o.strategy_name for strategy_o in all_strategies_o}
            context = {'all_strategies': json.dumps(all_strategies_dict, ensure_ascii=False)}
            return render(request, 'strategy/financial_data.html', context)
    except ServerException, e:
        response['errcode'] = e.err_code
        response['errmsg'] = e.err_msg
    except Exception, e:
        response['errcode'] = SERVER_ERR_INTERNAL
        response['errmsg'] = exception_string(e)
        print response['errmsg']

    return HttpResponse(json.dumps(response, ensure_ascii=False))


def financial_strategy_add(request):
    response = {}
    try:
        if request.method == 'POST':
            strategy_name = request.POST.get('strategyName')
            indicators = request.POST.get('indicatorList')
            indicator_list = [tuple(indicator.split('_')) for indicator in indicators.split(',')]
            rpcserver.rpc_financial_strategy_add(None, strategy_name, indicator_list)
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        else:
            context = {'all_indicators_json': FinanceIndicator.all_indicators_json()}
            return render(request, 'strategy/strategy_add.html', context)
    except ServerException, e:
        response['errcode'] = e.err_code
        response['errmsg'] = e.err_msg
    except Exception, e:
        response['errcode'] = SERVER_ERR_INTERNAL
        response['errmsg'] = exception_string(e)
        print response['errmsg']

    return HttpResponse(json.dumps(response, ensure_ascii=False))
