# -*- coding: utf-8 -*-
from django.db import models

class host(models.Model):
    when_created = models.DateTimeField(u"创建时间", null=True, auto_now_add=True)
    ip = models.CharField(u"",max_length=128)
    name = models.CharField(u"",max_length=128)
    system = models.CharField(u"",max_length=128)
    yun = models.CharField(u"",max_length=128)
    yun_id = models.CharField(u"",max_length=128,default="")
    biz = models.CharField(u"",max_length=128)
    biz_id = models.CharField(u"",max_length=128,default="")
    other = models.TextField(u"",default="")

class FuZai(models.Model):
    when_created = models.DateTimeField(u"创建时间", null=True, auto_now_add=True)
    ip = models.CharField(u"",max_length=128)
    value = models.CharField(u"",max_length=128)

