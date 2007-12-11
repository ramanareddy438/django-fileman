# -*- coding: utf-8 -*-

from django import newforms as forms
import os.path

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
            errors.append("Не указан путь")
        if len(self.files) == 0:
            errors.append("Нет файлов")
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