# -*- coding: utf-8 -*-

from fileman.models import ACTIONS, History
import os
import shutil

class File:
    def __init__(self, name = None, path = None, isdir = None, size = None):
        self.name = name
        self.path = path
        self.isdir = isdir
        self.size = size
    def __cmp__(self, other):
        return cmp(self.name, other.name)

def createHistory(author, action, *files):
    history = History()
    history.author = author
    history.action = ACTIONS[action] % files
    history.save()
    
class Fmoper:
    def existname(self, dst):
        i = 1
        if os.path.isfile(dst):
            dirname = os.path.dirname(dst)
            filename = os.path.basename(dst)
            name, ext = os.path.splitext(filename)
            while os.path.exists(dst):
                dst = os.path.join(dirname, "%s(copy%d)%s" % (name, i, ext))
                i += 1
        elif os.path.isdir(dst):
            dirname = os.path.dirname(dst)
            while os.path.exists(dst):
                dst = "%s(copy%d)" % (dirname, i)
                i += 1
        return dst
        
    def move(self, src, dst, replace = False):
        if not replace and os.path.exists(dst):
            dst = self.existname(dst)
        return shutil.move(src, dst)
        
    def copy(self, src, dst, replace = False):
        if not replace and os.path.exists(dst):
            dst = self.existname(dst) 
        if os.path.isfile(src):
            return shutil.copy(src, dst)
        else:
            return shutil.copytree(src, dst)
        
    def remove(self, path):
        if os.path.isdir(path):
            return shutil.rmtree(path)
        else:
            return os.remove(path)
