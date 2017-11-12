from django.template.loader import get_template
from django.http import HttpResponse

import json

import logging

logger = logging.getLogger('strategy')


def li_basic(request):
    response = {}
    if request.method == 'POST':
        code = request.POST.get('code')
        nyears = request.POST.get('nyears')
        data = {
            'rowTitles': ['Chinese', 'Math'],
            'colTitles1': ['Lucy', 'Jam'],
            'colTitles2': ['2010', '2011', '2012'],
            'tableData': {
                'Lucy': {
                    '2010': {'Chinese': 95, 'Math': 88},
                    '2011': {'Chinese': 96, 'Math': 89},
                    '2012': {'Chinese': 97, 'Math': 90},
                },
                'Jam': {
                    '2010': {'Chinese': 55, 'Math': 48},
                    '2011': {'Chinese': 56, 'Math': 49},
                    '2012': {'Chinese': 57, 'Math': 40},
                }
            },
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False))
    else:
        t = get_template('strategy/li_basic.html')
        html = t.render(response)
        return HttpResponse(html)
