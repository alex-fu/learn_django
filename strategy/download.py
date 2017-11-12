from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import render
import json

import logging

import error


logger = logging.getLogger('strategy')


def index(request):
    return render(request, 'strategy/download.html')


def get_data(request):
    return HttpResponse(json.dumps({'name': 'Welcome Julia'}, ensure_ascii=False))
