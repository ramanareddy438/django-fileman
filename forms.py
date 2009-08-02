# -*- coding: utf-8 -*-

from django import forms
import os.path
from fileman.utils import createHistory

from django.utils.translation import ugettext as _

class UploadForm:
    def __init__(self, data):
        self.errors = []
        if data.has_key('path'):
            self.path = data['path']
        else:
            self.path = None
        self.files = []
        i = 1;
        while 1:
            if not data.has_key('ufile%d' % i):
                break
            self.files.append(data['ufile%d' % i])
            i+=1
        
    def is_valid(self):
        if self.path is None:
            self.errors.append(_(u"Path does not set."))
        if len(self.files) == 0:
            self.errors.append(_(u"No files"))
        if len(self.errors) > 0:
            return False
        else:
            return True
        
    def save(self, request):
        for file in self.files:
            self.handle_uploaded_file(file)
            createHistory(request.user, "add", os.path.join(self.path, file.name))
        return True
        
    def handle_uploaded_file(self, f):
        destination = open(os.path.join(self.path, f.name), 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
