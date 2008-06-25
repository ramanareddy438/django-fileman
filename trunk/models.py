# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from fileman.fields import AutoForeignKey

from django.utils.translation import ugettext as _

ACTIONS = {"add": _(u"Upload file %s"),
    "rename": u"Rename file %s to %s",
    "delete": _(u"Delete file %s"),
    "destraction": _(u"Destroy file %s")}

class Setting(models.Model):
    owner = AutoForeignKey(User, unique=True, related_name='fileman_Setting')
    root = models.CharField(max_length=250, null=True)
    home = models.CharField(max_length=250, null=True)
    buffer = models.TextField(blank=True)
    class Admin:
        list_display = ('owner', 'root', 'home')
    class Meta:
        permissions = (
            ("can_fm_list", _("Can look files list")),
            ("can_fm_add", _("Can upload files")),
            ("can_fm_rename", _("Can rename files")),
            ("can_fm_del", _("Can move files to basket")),
            ("can_fm_destruct", _("Can delete files")),
        )
    def __unicode__(self):
        return unicode(self.owner)
    def __init__(self, *args, **kwargs):
        super(Setting, self).__init__(*args, **kwargs)
        if not self.root:
            self.root = None
            self.home = None
    def writeBuffer(self, data):
        self.buffer = data
        self.save()
            
        
class History(models.Model):
    action = models.CharField(max_length=250)
    author = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    class Admin:
        list_display = ('action', 'date', 'author')
        list_filter = ('date',)
    class Meta:
        verbose_name_plural = "History"
    def __unicode__(self):
        return self.action
    
class Alias(models.Model):
    path = models.CharField(max_length=250)
    url = models.CharField(max_length=250)
    class Admin:
        pass
    class Meta:
        verbose_name_plural = "Alias"
    def __unicode__(self):
        return self.url
