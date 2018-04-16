# -*- coding: utf-8 -*-

from django.conf.urls import url

# from . import download
from . import data


urlpatterns = [
    url(r'^$', data.financial_data, name="strategy_homepage"),

    # url(r'^download/$', download.index, name="strategy_download"),
    # url(r'^download_get_data/$', download.get_data, name="strategy_download_get_data"),

    url(r'^data/$', data.financial_data, name="strategy_data"),
    url(r'^financial_data/$', data.financial_data, name="strategy_financial_data"),
    url(r'^financial_add/$', data.financial_strategy_add, name="strategy_financial_add"),
    url(r'^financial_update/$', data.financial_strategy_update, name="strategy_financial_update"),
]
