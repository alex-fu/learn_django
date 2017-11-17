# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from error import *


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
        except ObjectDoesNotExist, e:
            raise ServerException(SERVER_ERR_FI_NOT_EXIST, repr(e))

    @staticmethod
    def financial_indicator_get_all_objects():
        return FinancialIndicatorModel.objects.all()

    @staticmethod
    def financial_indicator_query_objects(query_info):
        return FinancialIndicatorModel.objects.filter(**query_info)

    @staticmethod
    def financial_indicator_list_to_id_string(indicator_list, delimiter=','):
        indicators = {(indicator_o.indicator_name, indicator_o.indicator_type): indicator_o.id
                      for indicator_o in FinancialIndicatorModel.financial_indicator_get_all_objects()}
        try:
            return delimiter.join([indicators[indicator] for indicator in indicator_list])
        except Exception, e:
            raise ServerException(SERVER_ERR_WRONG_PARAM,
                                  'wrong indicator.{}'.format(exception_string(e)))


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
        except ObjectDoesNotExist, e:
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
