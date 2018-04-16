# -*- coding: utf-8 -*-

import logging
import json
# from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import render

from common.error import *
from strategy import rpcserver
from strategy.financial_indicator import FinanceIndicator
from strategy.meta import ModelsRequest

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
    except ServerException as e:
        response['errcode'] = e.err_code
        response['errmsg'] = e.err_msg
    except Exception as e:
        response['errcode'] = SERVER_ERR_INTERNAL
        response['errmsg'] = exception_string(e)
        logger.error('unknown exception: {}'.format(response['errmsg']))

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
    except ServerException as e:
        response['errcode'] = e.err_code
        response['errmsg'] = e.err_msg
    except Exception as e:
        response['errcode'] = SERVER_ERR_INTERNAL
        response['errmsg'] = exception_string(e)
        logger.error('unknown exception: {}'.format(response['errmsg']))

    return HttpResponse(json.dumps(response, ensure_ascii=False))


def financial_strategy_update(request):
    response = {}
    try:
        if request.method == 'POST':
            strategy_id = request.POST.get('strategyId')
            operation = request.POST.get('operation')
            if operation == 'show':
                # get strategy info
                response['indicators'] = [indicator_type + '_' + indicator_name for indicator_type, indicator_name
                                          in ModelsRequest.financial_strategy_get_object(strategy_id)]
            elif operation == 'delete':
                # delete strategy
                rpcserver.rpc_financial_strategy_delete(None, strategy_id)
            elif operation == 'copy':
                # copy strategy
                new_strategy_name = request.POST.get('newStrategyName')
                rpcserver.rpc_financial_strategy_copy(None, new_strategy_name, strategy_id)
            elif operation == 'update':
                # update strategy
                indicators = request.POST.get('indicatorList')
                indicator_list = [tuple(indicator.split('_')) for indicator in indicators.split(',')]
                rpcserver.rpc_financial_strategy_update(None, strategy_id, indicator_list)
            else:
                raise ServerException(SERVER_ERR_INTERNAL, 'unknown operation: {}'.format(operation))
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        else:
            all_strategies_o = ModelsRequest.financial_strategy_get_all_objects()
            all_strategies_dict = {strategy_o.id: strategy_o.strategy_name for strategy_o in all_strategies_o}
            context = {'all_indicators_json': FinanceIndicator.all_indicators_json(),
                       'all_strategies': json.dumps(all_strategies_dict, ensure_ascii=False)}
            return render(request, 'strategy/strategy_update.html', context)
    except ServerException as e:
        response['errcode'] = e.err_code
        response['errmsg'] = e.err_msg
    except Exception as e:
        response['errcode'] = SERVER_ERR_INTERNAL
        response['errmsg'] = exception_string(e)
        logger.error('unknown exception: {}'.format(response['errmsg']))

    return HttpResponse(json.dumps(response, ensure_ascii=False))
