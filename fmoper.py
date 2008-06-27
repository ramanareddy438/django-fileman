# -*- coding: utf-8 -*-

import os
import shutil

def existname(dst):
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
    
def move(src, dst, replace=False):
    if not replace and os.path.exists(dst):
        dst = existname(dst)
    return shutil.move(src, dst)
    
def copy(src, dst, replace=False):
    if not replace and os.path.exists(dst):
        dst = existname(dst) 
    if os.path.isfile(src):
        return shutil.copy(src, dst)
    else:
        return shutil.copytree(src, dst)
    
def remove(path):
    if os.path.isdir(path):
        return shutil.rmtree(path)
    else:
        return os.remove(path)
