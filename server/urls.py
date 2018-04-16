# coding=utf-8

"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from jsonrpc import jsonrpc_site

from . import file_download
# from app_strategy import rpcserver
from app_crawler import rpc

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^json/$', jsonrpc_site.dispatch, name="json_rpc"),
    url(r'^file_download/', file_download.file_download, name="file_download"),

    # url(r'^strategy/', include('app_strategy.urls', namespace='strategy')),
]
