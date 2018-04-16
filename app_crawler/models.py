# -*- coding: utf-8 -*-

from django.db import models
from jsonfield import JSONField
from django.core.exceptions import ObjectDoesNotExist

from common import error


# Create your models here.
class CrawlerModel(models.Model):
    code = models.CharField(max_length=8, primary_key=True)
    detail = JSONField(default=dict)

    class Meta:
        db_table = 'crawler'

    @staticmethod
    def crawler_object(code):
        try:
            return CrawlerModel.objects.get(code=code)
        except ObjectDoesNotExist as e:
            raise error.ServerException(error.SERVER_ERR_OBJECT_NOT_EXIST, error.exception_string(e))

    @staticmethod
    def crawler_objects_all():
        return CrawlerModel.objects.all()

    @staticmethod
    def crawler_objects_filter(**kwargs):
        return CrawlerModel.objects.filter(**kwargs)
