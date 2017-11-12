# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class BasicModel(models.Model):
    code = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=32, null=False, blank=False)
    up_to_market = models.CharField(max_length=8, null=False, blank=False)

    class Meta:
        db_table = 'basic'


class ReportModel(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.ForeignKey(BasicModel, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        db_table = 'report'
