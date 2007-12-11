# -*- coding: utf-8 -*-

from fileman.models import ACTIONS, History

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