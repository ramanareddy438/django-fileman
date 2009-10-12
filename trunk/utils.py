# -*- coding: utf-8 -*-

from fileman.models import ACTIONS, History
from fileman.settings import *

def toUnicode(string):
    if not type(string) == type(u''):
        string = string.decode(ENCODING)
    return string

def toString(string):
    if type(string) == type(u''):
        string = string.encode(ENCODING)
    return string

class File:
    def __init__(self, name=None, path=None, isdir=None, size=None):
        self.name = toUnicode(name)
        self.path = toUnicode(path)
        self.isdir = isdir
        self.size = size
    def __cmp__(self, other):
        return cmp(self.name, other.name)

def createHistory(author, action, *files):
    history = History()
    history.author = author
    history.action = ACTIONS[action] % files
    history.save()

