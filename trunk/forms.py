# -*- coding: utf-8 -*-

from django import newforms as forms
import os.path

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
        
    def save(self):
        for file in self.files:
            f = open(os.path.join(self.path, file['filename']), 'w')
            f.write(file['content'])
            f.close()
            createHistory(request.user, "add", os.path.join(self.path, file['filename']))
        return True
