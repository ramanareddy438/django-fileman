# -*- coding: utf-8 -*-

from fileman.settings import *
from fileman.models import Setting, Alias
from fileman.forms import UploadForm
from fileman.utils import File, createHistory

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

import os
import pickle, re
import operator
import shutil

from django.utils.translation import ugettext as _

def raise_error(request, msg):
        return render_to_response('error.html',
                       {"msg": msg},
                        context_instance=RequestContext(request))

@login_required
def list(request, path = None):
    if request.user.fileman_Setting.home is None or request.user.fileman_Setting.root is None:
        return raise_error(request,
            [_("Не назначена корневая или домашняя директория")])
    if path is None:
        path = request.user.fileman_Setting.home
    if not os.path.exists(path):
        return raise_error(request,
            [_("Несуществующий путь")])
    if re.search("^%s" % request.user.fileman_Setting.root, path) is None:
        return raise_error(request,
            [_("Нет доступа")])
        
    dirlist = []
    filelist = []
    for f in os.listdir(path):
        file = File(f, "%s/%s" % (path, f))
        if os.path.isdir(os.path.join(path, f)):
            file.isdir = 1
            file.size = "Dir"
            dirlist.append(file)
        else:
            file.isdir = 0
            file.size = os.path.getsize(os.path.join(path, f))
            filelist.append(file)
        dirlist.sort()
        filelist.sort()
            
    buffer = listBuffer(request)
    for item in buffer:
        item.append(os.path.basename(item[0]))
    return render_to_response('list.html',
           {"pwd": path,
            "dirlist": dirlist,
            "filelist": filelist,
            "buffer": buffer,
            },
            context_instance=RequestContext(request))
list = permission_required('fileman.can_fm_list')(list)
        
@login_required
def upload(request):
    if request.POST:
        post_data = request.POST.copy()
        if re.search("^%s" % request.user.fileman_Setting.root, post_data['path']) is None:
            return raise_error(request,
                [_("Нет доступа")])
        post_data.update(request.FILES)
        form = UploadForm(post_data)
        print 1
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/fm/list/%s' % form.path)
        else:
            return raise_error(request,
                [form.errors])
    else:
        return raise_error(request,
                [_("Пустая форма")])
upload = permission_required('fileman.can_fm_add')(upload)
    
@login_required
def preview(request, path = None):
    if path is None:
        return HttpResponse(_("Не указан путь."))
    if re.search("^%s" % request.user.fileman_Setting.root, path) is None:
        return raise_error(request,
            [_("Нет доступа")])
    from PIL import Image
    size = 176, 176
    im = Image.open(path)
    im.thumbnail(size, Image.ANTIALIAS)
    response = HttpResponse(mimetype="image/png")
    im.save(response, "PNG")
    return response
    
@login_required
def getUrl(request, path = None):
    if path is None:
        return HttpResponse(_("Не указан путь."))
    if re.search("^%s" % request.user.fileman_Setting.root, path) is None:
        return raise_error(request,
                [_("Нет доступа")])
    for alias in Alias.objects.all():
        if path.startswith(alias.path):
            return HttpResponse(path.replace(alias.path, alias.url))
    return HttpResponse(_("Нет доступа из вне"))
    
@login_required
def delete(request):
    if request.POST:
        if request.GET.has_key('next'):
            path = request.GET['next']
        else:
            path = ''
        for key in request.POST.keys():
            if re.search("^%s" % request.user.fileman_Setting.root, request.POST[key]) is None:
                return raise_error(request,
                    [_("Нет доступа")])
            try:
                os.rename(request.POST[key], "%s/%s" % (BASKET_FOLDER, os.path.split(request.POST[key])[1]))
            except Exception, msg:
                if request.GET.has_key('xhr'):
                    return HttpResponse(msg)
                return raise_error(request,
                    [msg])
            createHistory(request.user, "delete", request.POST[key])
        if request.GET.has_key('xhr'):
            return HttpResponse("success")
        return HttpResponseRedirect('/fm/list/%s' % path)
    else:
        return raise_error(request,
            [_("Пустая форма")])
delete = permission_required('fileman.can_fm_del')(delete)
                
@login_required
def destraction(request):
    if request.POST:
        if request.GET.has_key('next'):
            path = request.GET['next']
        else:
            path = ''
        for key in request.POST.keys():
            if re.search("^%s" % request.user.fileman_Setting.root, request.POST[key]) is None:
                return raise_error(request,
                    [_("Нет доступа")])
            if os.path.isdir(request.POST[key]):
                try:
                    rmdir(request.POST[key])
                except Exception, msg:
                    if request.GET.has_key('xhr'):
                        return HttpResponse(msg)
                    return raise_error(request,
                        [msg])
            else:
                try:
                    os.remove(request.POST[key])
                except Exception, msg:
                    if request.GET.has_key('xhr'):
                        return HttpResponse(msg)
                    return raise_error(request,
                        [msg])
                createHistory(request.user, "destraction", request.POST[key])
        if request.GET.has_key('xhr'):
            return HttpResponse("success")
        return HttpResponseRedirect('/fm/list/%s' % path)
    else:
        return raise_error(request,
            [_("Пустая форма")])
destraction = permission_required('fileman.can_fm_destruct')(destraction)
                
@login_required
def rmdir(path):
    if re.search("^%s" % request.user.fileman_Setting.root, path) is None:
        return raise_error(request,
            [_("Нет доступа")])
    for f in os.listdir(path):
        if os.path.isdir(os.path.join(path, f)):
            rmdir(os.path.join(path, f))
        else:
            os.remove(os.path.join(path, f))
    os.rmdir(path)
rmdir = permission_required('fileman.can_fm_del')(rmdir)
                
def move(request):
    pass

@login_required
def rename(request, source = None, dest = None):
    if (source is None) and (dest is None):
        if request.POST:
            if request.GET.has_key('next'):
                path = request.GET['next']
            else:
                path = ''
            for key in request.POST.keys():
                if re.search("^%s" % request.user.fileman_Setting.root, request.POST[key]) is None:
                    return raise_error(request,
                        [_("Нет доступа")])
            return HttpResponseRedirect('/fm/list/%s' % path)
        else:
            return raise_error(request,
                [_("Пустая форма")])
    else:
        shutil.move(source, dest)
        createHistory(request.user, "rename", source, dest)
rename = permission_required('fileman.can_fm_rename')(rename)
                
@login_required
def createDir(request, path = None):
    if path is None:
        return HttpResponse(_("Не указан путь."))
    os.mkdir(path)
    return HttpResponseRedirect('/fm/list/%s' % path)
createDir = permission_required('fileman.can_fm_add')(createDir)

@login_required
def addBuffer(request):
    if request.POST:
        path = request.POST['path']
        if re.search("^%s" % request.user.fileman_Setting.root, path) is None:
            return raise_error(request,
                    [_("Нет доступа")])
        if request.POST['action'] == "copy":
            action = 1
        elif request.POST['action'] == "cut":
            action = 2
        buffer =  listBuffer(request)
        if not [path, 1] in buffer and not [path, 2] in buffer:
            buffer.append([path, action])
        request.user.fileman_Setting.writeBuffer(pickle.dumps(buffer))
        if request.GET.has_key('xhr'):
            return HttpResponse("success")
    else:
        return raise_error(request,
            [_("Пустая форма")])
                
@login_required
def listBuffer(request):
    if request.user.fileman_Setting.buffer != "":
        buffer = pickle.loads(request.user.fileman_Setting.buffer.encode("utf8"))
    else:
        buffer = []
    return buffer
    
@login_required
def clearBuffer(request):
    request.user.fileman_Setting.writeBuffer("")
    
@login_required
def past(request, path = None):
    if path is None:
        return HttpResponse(_("Не указан путь."))
    if re.search("^%s" % request.user.fileman_Setting.root, path) is None:
        return raise_error(request,
                    [_("Нет доступа")])
    buffer = listBuffer(request)
    for item in buffer:
        to = os.path.basename(item[0])
        if os.path.exists(os.path.join(path, to)):
            to = os.path.splitext(to)[0]+"_1"+os.path.splitext(to)[1]
        i=2
        while os.path.exists(os.path.join(path, to)):
            to = os.path.splitext(to)[0][:-1]+str(i)+os.path.splitext(to)[1]
            i+=1
        if item[1] == 1:
            shutil.copy(item[0], os.path.join(path, to))
        elif item[1] == 2:
            rename(request, item[0], os.path.join(path, to))
    clearBuffer(request)
    return HttpResponseRedirect('/fm/list/%s' % path)
past = permission_required('fileman.can_fm_rename')(past)

@login_required
def RemoveFromBuffer(request, path = None):
    if path is None:
        return HttpResponse(_("Не указан путь."))
    if re.search("^%s" % request.user.fileman_Setting.root, path) is None:
        return raise_error(request,
                    [_("Нет доступа")])
    buffer =  listBuffer(request)
    if [path, 1] in buffer:
        buffer.remove([path, 1])
    elif [path, 2] in buffer:
        buffer.remove([path, 2])
    request.user.fileman_Setting.writeBuffer(pickle.dumps(buffer))
    return HttpResponse("success")
    
@login_required
def listBasket(request):
    return list(request, BASKET_FOLDER)
listBasket = permission_required('fileman.can_fm_del')(listBasket)