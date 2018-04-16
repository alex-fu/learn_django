# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from common.error import *


class FinancialIndicatorModel(models.Model):
    id = models.AutoField(primary_key=True)
    indicator_type = models.CharField(max_length=64, null=False, blank=False)
    indicator_name = models.CharField(max_length=128, null=False, blank=False)

    class Meta:
        db_table = 'financial_indicator'
        unique_together = (('indicator_type', 'indicator_name'),)

    @staticmethod
    def financial_indicator_get_object(indicator_id):
        try:
            return FinancialIndicatorModel.objects.get(id=indicator_id)
        except ObjectDoesNotExist as e:
            raise ServerException(SERVER_ERR_FI_NOT_EXIST, repr(e))

    @staticmethod
    def financial_indicator_get_all_objects():
        return FinancialIndicatorModel.objects.all()

    @staticmethod
    def financial_indicator_query_objects(query_info):
        return FinancialIndicatorModel.objects.filter(**query_info)

    @staticmethod
    def financial_indicator_list_to_id_string(indicator_list, delimiter=','):
        indicators = {(indicator_o.indicator_type, indicator_o.indicator_name): indicator_o.id
                      for indicator_o in FinancialIndicatorModel.financial_indicator_get_all_objects()}
        try:
            indicator_id_list = [indicators[indicator] for indicator in indicator_list]
            indicator_id_unique_list = []
            indicator_id_set = set()
            for indicator_id in indicator_id_list:
                if indicator_id not in indicator_id_set:
                    indicator_id_unique_list.append(indicator_id)
                    indicator_id_set.add(indicator_id)
            return delimiter.join([str(indicator_id) for indicator_id in indicator_id_unique_list])
        except Exception as e:
            raise ServerException(SERVER_ERR_WRONG_PARAM,
                                  'wrong indicator.{}'.format(exception_string(e)))

    @staticmethod
    def financial_indicator_id_to_list(indicator_id_str, delimiter=','):
        indicators = {indicator_o.id: (indicator_o.indicator_type, indicator_o.indicator_name)
                      for indicator_o in FinancialIndicatorModel.financial_indicator_get_all_objects()}
        try:
            return [indicators[int(indicator_id)] for indicator_id in indicator_id_str.split(delimiter)]
        except Exception as e:
            raise ServerException(SERVER_ERR_WRONG_PARAM,
                                  'wrong indicator id.{}'.format(exception_string(e)))


class FinancialStrategyModel(models.Model):
    id = models.AutoField(primary_key=True)
    strategy_name = models.CharField(max_length=128, null=False, blank=False)
    indicators = models.TextField(null=False, blank=False)

    class Meta:
        db_table = 'financial_strategy'

    @staticmethod
    def financial_strategy_get_object(indicator_id):
        try:
            return FinancialStrategyModel.objects.get(id=indicator_id)
        except ObjectDoesNotExist as e:
            raise ServerException(SERVER_ERR_FI_NOT_EXIST, repr(e))

    @staticmethod
    def financial_strategy_get_all_objects():
        return FinancialStrategyModel.objects.all()

    @staticmethod
    def financial_strategy_query_objects(query_info):
        return FinancialStrategyModel.objects.filter(**query_info)


# class BasicModel(models.Model):
#     code = models.CharField(max_length=8, primary_key=True)
#     name = models.CharField(max_length=32, null=False, blank=False)
#     up_to_market = models.CharField(max_length=8, null=False, blank=False)
#
#     class Meta:
#         db_table = 'basic'
#
#
# class ReportModel(models.Model):
#     id = models.AutoField(primary_key=True)
#     code = models.ForeignKey(BasicModel, on_delete=models.CASCADE, blank=False, null=False)
#
#     class Meta:
#         db_table = 'report'
