# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from blog.fields import AutoOneToOneField

ACTIONS = {"add": "Загрузка файла %s",
    "rename": "Переименование файла %s в %s",
    "delete": "Перемещение в корзину файла %s",
    "destruction": "Удаление файла %s"}

class Setting(models.Model):
    owner = AutoOneToOneField(User, related_name='fileman_Setting')
    root = models.CharField(maxlength=250, null=True)
    home = models.CharField(maxlength=250, null=True)
    buffer = models.TextField(blank=True)
    class Admin:
        pass
    class Meta:
        permissions = (
            ("can_fm_list", "Can look files list"),
            ("can_fm_add", "Can upload files"),
            ("can_fm_rename", "Can rename files"),
            ("can_fm_del", "Can move files to basket"),
            ("can_fm_destruct", "Can delete files"),
        )
    def __unicode__(self):
        return str(self.owner)
    def __init__(self, *args, **kwargs):
        super(Setting, self).__init__(*args, **kwargs)
        if not self.root:
            self.root = None
            self.home = None
    def writeBuffer(self, data):
        self.buffer = data
        self.save()
            
        
class History(models.Model):
    action = models.CharField(maxlength=250)
    author = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    class Admin:
        pass
    def __unicode__(self):
        return str(self.action)
    
class Alias(models.Model):
    path = models.CharField(maxlength=250)
    url = models.CharField(maxlength=250)
    class Admin:
        pass
    def __unicode__(self):
        return str(self.url)