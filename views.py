# -*- coding: utf-8 -*-

from fileman.settings import *
# import models
from fileman.models import Setting, Alias 
from django.contrib.auth.models import User
# import utils
from fileman.forms import UploadForm
from fileman.utils import File, createHistory
# import django functions
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
# import decorators
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from functools import wraps
# import filesystem and others main modules
import os, mimetypes, shutil
import pickle, re
import operator
from fileman.utils import Fmoper
from django.utils import simplejson
from django.core.servers.basehttp import FileWrapper
# import internationalization
from django.utils.translation import ugettext as _
from pytils.translit import slugify

fmoper = Fmoper() # Create file manager object

###                 Decorators              ###
def rightPath(fn):
    @wraps(fn)
    def wrapper(request, *args, **kw):
        if "path" in kw:
            path = kw["path"]
            if path is None:
                return raise_error(request,
                    [_(u"Path does not set.")])
            if re.search("^%s" % request.user.fileman_Setting.root, path) is None:
                return raise_error(request,
                    [_(u"No access")])
            if not os.path.exists(path):
                return raise_error(request,
                    [_(u"Path does not exist.")])
        return fn(request, *args, **kw)
    return wrapper

###                 Render                  ###
def raise_error(request, msg):
    if request.is_ajax():
        return json({'status': "error", "msg": msg})
    return render_to_response('error.html',
               {"msg": msg},
                context_instance=RequestContext(request))
                
def json(data = None):
    if data is None:
        data = {}
    if not type(data) == type(dict()):
        raise Exception('ajax TypeError')
    if 'status' not in data:
        data['status'] = "success"
    json = simplejson.dumps(data)
    return HttpResponse(json, mimetype='application/json')

def ls(request, path = None):
    """ Render file list """
    if request.user.fileman_Setting.home is None or request.user.fileman_Setting.root is None:
        return raise_error(request,
            [_(u"Root or home directory is not set.")])
    if path is None:
        path = request.user.fileman_Setting.home
    if not os.path.exists(path):
        return raise_error(request,
            [_(u"Path does not exist.")])
    if re.search("^%s" % request.user.fileman_Setting.root, path) is None:
        return raise_error(request,
            [_(u"No access")])
        
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
    
    anonymous = False
    if request.user == User.objects.get(username="Anonymous"):
        anonymous = True
    return render_to_response('list.html',
           {"pwd": path,
            "dirlist": dirlist,
            "filelist": filelist,
            "buffer": buffer,
            "anonymous": anonymous,
            },
            context_instance=RequestContext(request))
ls = permission_required('fileman.can_fm_list')(ls)

def listBasket(request):
    """ Render Recycle Bin """
    return ls(request, BASKET_FOLDER)
listBasket = permission_required('fileman.can_fm_del')(listBasket)

@rightPath
def view(request, path = None):
    """ Render single file """
    name, ext = os.path.splitext(os.path.basename(path))
    if ext in TEXT_EXT:
        f = open(path, 'r')
        data = f.readlines()
        f.close()
        return render_to_response('view_text.html',
           {"pwd": path,
            "data": file(path, "rb").read()
            },
            context_instance=RequestContext(request))
    elif ext in PICTURE_EXT:
        return render_to_response('view_picture.html',
           {"pwd": path,
            },
            context_instance=RequestContext(request))
    else:
        return download(request, path)
view = permission_required('fileman.can_fm_list')(view)

###             Actions with files          ###
def upload(request):
    if request.POST:
        post_data = request.POST.copy()
        if re.search("^%s" % request.user.fileman_Setting.root, post_data['path']) is None:
            return raise_error(request,
                [_(u"No access")])
        post_data.update(request.FILES)
        form = UploadForm(post_data)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/fm/list/%s' % form.path)
        else:
            return raise_error(request,
                form.errors)
    else:
        return raise_error(request,
                [_(u"Empty form.")])
upload = permission_required('fileman.can_fm_add')(upload)

@rightPath
def delete(request, path, inside = False):
    try:
        fmoper.move(path, "%s/%s" % (BASKET_FOLDER, os.path.basename(path)))
    except Exception, msg:
        return raise_error(request, [msg])
    createHistory(request.user, "delete", path)
    if request.is_ajax():
        return json({"status": "success"})
    else:
        return ls(request, os.path.dirname(path))
delete = permission_required('fileman.can_fm_del')(delete)

def delete2(request):
    if request.POST:
        if request.GET.has_key('next'):
            next = request.GET['next']
        else:
            next = ''
        for key in request.POST.keys():
            try:
                fmoper.move(request.POST[key], "%s/%s" % (BASKET_FOLDER, os.path.basename(request.POST[key])))
            except Exception, msg:
                return raise_error(request, [msg])
            createHistory(request.user, "destraction", request.POST[key])
        if request.is_ajax():
            return json({"status": "success"})
        return HttpResponseRedirect('/fm/list/%s' % next)
    else:
        return raise_error(request,
            [_(u"Empty form.")])
delete2 = permission_required('fileman.can_fm_del')(delete2)
                
@rightPath
def destraction(request, path):
    try:
        fmoper.remove(path)
    except Exception, msg:
            return raise_error(request, [msg])  
    createHistory(request.user, "destraction", path)  
    if request.is_ajax():
        return json({"status": "success"})
    else:
        return ls(request, os.path.dirname(path))
destraction = permission_required('fileman.can_fm_destruct')(destraction)
    
def destraction2(request):
    if request.POST:
        if request.GET.has_key('next'):
            next = request.GET['next']
        else:
            next = ''
        for key in request.POST.keys():
            try:
                fmoper.remove(request.POST[key])
            except Exception, msg:
                return raise_error(request, [msg])
            createHistory(request.user, "destraction", request.POST[key])
        if request.is_ajax():
            return json({"status": "success"})
        return HttpResponseRedirect('/fm/list/%s' % next)
    else:
        return raise_error(request,
            [_(u"Empty form.")])
destraction2 = permission_required('fileman.can_fm_destruct')(destraction2)

@rightPath
def rename(request, path = None, newName = None):
    if path is None:
        return raise_error(request,
                [_(u"Input error")])
    if newName is None:
        if request.GET.has_key('newname'):
            newName = request.GET['newname']
        else:
            return raise_error(request,
                    [_(u"Input error")])
    dest = os.path.join(os.path.dirname(path), newName)
    fmoper.move(path, dest)
    createHistory(request.user, "rename", path, dest)
    if request.GET.has_key('next'):
        next = request.GET['next']
    else:
        next = ''
    if request.is_ajax():
        return json({"status": "success", "path": dest})
    return HttpResponseRedirect('/fm/list/%s' % next)
rename = permission_required('fileman.can_fm_rename')(rename)
                
def createDir(request, path = None):
    if path is None:
        return HttpResponse(_(u"Path does not set."))
    os.mkdir(path)
    return HttpResponseRedirect('/fm/list/%s' % path)
createDir = permission_required('fileman.can_fm_add')(createDir)

###                  Buffer                 ###
@login_required
def addBuffer(request):
    if request.POST:
        path = request.POST['path']
        if re.search("^%s" % request.user.fileman_Setting.root, path) is None:
            return raise_error(request,
                    [_(u"No access")])
        if request.POST['action'] == "copy":
            action = 1
        elif request.POST['action'] == "cut":
            action = 2
        buffer =  listBuffer(request)
        if not [path, 1] in buffer and not [path, 2] in buffer:
            buffer.append([path, action])
            request.user.fileman_Setting.writeBuffer(pickle.dumps(buffer))
        else:
            return raise_error(request,
                    [_(u"File is already in buffer")])
        if request.is_ajax():
            return json({"status": "success", "path": path})
        return ls(request)
    else:
        return raise_error(request,
            [_(u"Empty form.")])
                

def listBuffer(request):
    if request.user.fileman_Setting.buffer != "":
        buffer = pickle.loads(request.user.fileman_Setting.buffer.encode("utf8"))
    else:
        buffer = []
    return buffer
    
@login_required
def clearBuffer(request):
    request.user.fileman_Setting.writeBuffer("")
    
@rightPath
def past(request, path = None):
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

@rightPath
def RemoveFromBuffer(request, path = None):
    buffer = listBuffer(request)
    if [path, 1] in buffer:
        buffer.remove([path, 1])
    elif [path, 2] in buffer:
        buffer.remove([path, 2])
    request.user.fileman_Setting.writeBuffer(pickle.dumps(buffer))
    return json({"status": "success"})
    
###                  Others                 ###
@rightPath
def preview(request, path = None, size = (176, 176)):
    from PIL import Image
    im = Image.open(path)
    im.thumbnail(size, Image.ANTIALIAS)
    response = HttpResponse(mimetype="image/png")
    im.save(response, "PNG")
    return response
preview = permission_required('fileman.can_fm_list')(preview)
    
@rightPath
def getUrl(request, path = None):
    for alias in Alias.objects.all():
        if path.startswith(alias.path):
            url = path.replace(alias.path, alias.url)
            if request.is_ajax():
                return json({"status": "success", "url": url})
            return HttpResponse(url)
    if request.is_ajax():
        return json({"status": "error"})
    return HttpResponse(_(u"No access."))
    
@rightPath
def image(request, path = None):
    return preview(request, path, (800, 2000))
image = permission_required('fileman.can_fm_list')(image)

@rightPath
def download(request, path = None, filename = None, mimetype = None):
    if filename is None: filename = os.path.basename(path)
    if mimetype is None:
        mimetype, encoding = mimetypes.guess_type(filename)
    response = HttpResponse(FileWrapper(file(path)), mimetype=mimetype)
    response['Content-Disposition'] = "attachment; filename=%s" % slugify(filename)
    response['Content-Length'] = os.path.getsize(path)
    return response
download = permission_required('fileman.can_fm_list')(download)
