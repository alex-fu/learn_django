# from multiprocessing.pool import ThreadPool
from django.db import transaction
from django.db.utils import IntegrityError
# from django.db.models.deletion import ProtectedError
import threading

from error import *


def exception_string(e):
    import traceback
    return '{}\n{}'.format(e, traceback.format_exc())


class ModelsRequest:
    # _pool = ThreadPool(1)
    _lock = threading.Lock()

    def __init__(self):
        raise RuntimeError('can not instance ModelsRequest')

    @staticmethod
    def _request(func, args):
        with ModelsRequest._lock:
            return func(*args)
        # return ModelsRequest._pool.apply(func, args=args)

    @staticmethod
    def financial_indicator_add(indicator_type, indicator_name):
        return ModelsRequest._request(_financial_indicator_add, args=(indicator_type, indicator_name,))

    @staticmethod
    def financial_indicator_import(indicators_dict):
        return ModelsRequest._request(_financial_indicator_import, args=(indicators_dict,))

    @staticmethod
    def financial_indicator_get_object(indicator_id):
        return ModelsRequest._request(_financial_indicator_get_object, args=(indicator_id,))

    @staticmethod
    def financial_indicator_get_all_objects():
        return ModelsRequest._request(_financial_indicator_get_all_objects, args=())

    @staticmethod
    def financial_indicator_query_objects(query_info):
        return ModelsRequest._request(_financial_indicator_query_objects, args=(query_info,))

    @staticmethod
    def financial_strategy_add(strategy_name, indicator_list):
        return ModelsRequest._request(_financial_strategy_add, args=(strategy_name, indicator_list,))

    @staticmethod
    def financial_strategy_update(strategy_id, indicator_list):
        return ModelsRequest._request(_financial_strategy_update, args=(strategy_id, indicator_list,))

    @staticmethod
    def financial_strategy_copy(strategy_name, old_strategy_id):
        return ModelsRequest._request(_financial_strategy_copy, args=(strategy_name, old_strategy_id,))

    @staticmethod
    def financial_strategy_get_object(strategy_id):
        return ModelsRequest._request(_financial_strategy_get_object, args=(strategy_id,))

    @staticmethod
    def financial_strategy_get_all_objects():
        return ModelsRequest._request(_financial_strategy_get_all_objects, args=())

    @staticmethod
    def financial_strategy_query_objects(query_info):
        return ModelsRequest._request(_financial_strategy_query_objects, args=(query_info,))


########################################################################################################################
# financial indicator operations
########################################################################################################################
@transaction.atomic
def _financial_indicator_add(indicator_type, indicator_name):
    from models import FinancialIndicatorModel
    try:
        indicator_o = FinancialIndicatorModel(indicator_type=indicator_type, indicator_name=indicator_name)
        indicator_o.save()
        return indicator_o
    except IntegrityError, e:
        raise ServerException(SERVER_ERR_FI_ALREADY_EXIST, exception_string(e))


@transaction.atomic
def _financial_indicator_import(indicator_dict):
    from models import FinancialIndicatorModel
    try:
        old_indicators = [(indicator_o.indicator_name, indicator_o.indicator_type)
                          for indicator_o in FinancialIndicatorModel.financial_indicator_get_all_objects()]
        for indicator_type, indicator_name_list in indicator_dict.items():
            for indicator_name in indicator_name_list:
                if (indicator_name, indicator_type) not in old_indicators:
                    indicator_o = FinancialIndicatorModel(indicator_type=indicator_type, indicator_name=indicator_name)
                    indicator_o.save()
    except IntegrityError, e:
        raise ServerException(SERVER_ERR_FI_ALREADY_EXIST, exception_string(e))


@transaction.atomic
def _financial_indicator_get_object(indicator_id):
    from models import FinancialIndicatorModel
    return FinancialIndicatorModel.financial_indicator_get_object(indicator_id)


@transaction.atomic
def _financial_indicator_get_all_objects():
    from models import FinancialIndicatorModel
    return FinancialIndicatorModel.financial_indicator_get_all_objects()


@transaction.atomic
def _financial_indicator_query_objects(query_info):
    from models import FinancialIndicatorModel
    return FinancialIndicatorModel.financial_indicator_query_objects(query_info)


########################################################################################################################
# financial strategy operations
########################################################################################################################
@transaction.atomic
def _financial_strategy_add(strategy_name, indicator_list):
    from models import FinancialIndicatorModel, FinancialStrategyModel
    select_indicators = FinancialIndicatorModel.financial_indicator_list_to_id_string(indicator_list)
    try:
        strategy_o = FinancialStrategyModel(strategy_name=strategy_name, indicators=select_indicators)
        strategy_o.save()
    except IntegrityError, e:
        raise ServerException(SERVER_ERR_FI_ALREADY_EXIST, exception_string(e))
    return strategy_o


@transaction.atomic
def _financial_strategy_update(strategy_id, indicator_list):
    from models import FinancialIndicatorModel, FinancialStrategyModel
    select_indicators = FinancialIndicatorModel.financial_indicator_list_to_id_string(indicator_list)
    try:
        strategy_o = FinancialStrategyModel.financial_strategy_get_object(strategy_id)
        strategy_o.indicators = select_indicators
        strategy_o.save()
    except IntegrityError, e:
        raise ServerException(SERVER_ERR_FI_ALREADY_EXIST, exception_string(e))
    return strategy_o


@transaction.atomic
def _financial_strategy_copy(strategy_name, old_strategy_id):
    from models import FinancialStrategyModel
    try:
        old_strategy_o = FinancialStrategyModel.financial_strategy_get_object(old_strategy_id)
        new_strategy_o = FinancialStrategyModel(strategy_name=strategy_name, indicators=old_strategy_o.indicators)
        new_strategy_o.save()
    except IntegrityError, e:
        raise ServerException(SERVER_ERR_FI_ALREADY_EXIST, exception_string(e))
    return new_strategy_o


@transaction.atomic
def _financial_strategy_get_object(strategy_id):
    from models import FinancialStrategyModel, FinancialIndicatorModel
    strategy_o = FinancialStrategyModel.financial_strategy_get_object(strategy_id)
    return FinancialIndicatorModel.financial_indicator_id_to_list(strategy_o.indicators)


@transaction.atomic
def _financial_strategy_get_all_objects():
    from models import FinancialStrategyModel
    return FinancialStrategyModel.financial_strategy_get_all_objects()


@transaction.atomic
def _financial_strategy_query_objects(query_info):
    from models import FinancialStrategyModel
    return FinancialStrategyModel.financial_strategy_query_objects(query_info)
