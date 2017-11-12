from django.conf.urls import url

import download
import data


urlpatterns = [
    url(r'^$', download.index, name="homepage"),

    url(r'^download/$', download.index, name="download"),
    url(r'^get_data/$', download.get_data, name="get_data"),

    url(r'^data/$', data.li_basic, name="data"),
    url(r'^li_basic/$', data.li_basic, name="li_basic"),
]
