import logging
import json
from django.template.loader import get_template
from django.http import HttpResponse

from error import *
import rpcserver

logger = logging.getLogger('strategy')


def li_basic(request):
    response = {}
    try:
        if request.method == 'POST':
            codes = request.POST.get('codes')
            dates = request.POST.get('dates')
            uuid, html = rpcserver.rpc_lijie_basic(None, {'codes': codes, 'dates': dates})
            response['table_data'] = html
            response['uuid'] = uuid
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        else:
            t = get_template('strategy/li_basic.html')
            html = t.render(response)
            return HttpResponse(html)
    except ServerException, e:
        response['errcode'] = e.err_code
        response['errmsg'] = e.err_msg
    except Exception, e:
        response['errcode'] = SERVER_ERR_INTERNAL
        response['errmsg'] = exception_string(e)

    return HttpResponse(json.dumps(response, ensure_ascii=False))
