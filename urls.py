from django.conf.urls.defaults import *
from fileman import views
import fileman.settings as settings

js_info_dict = {
    'packages': ('cyxapeff_org.fileman',),
}

urlpatterns = patterns('',
    (r'^media/jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^list/$', views.ls),
    url(r'^list/(?P<path>.+)/$', views.ls, name="ls_path"),
    (r'^preview/$', views.preview),
    (r'^preview/(?P<path>.+)$', views.preview),
    (r'^geturl/$', views.getUrl),
    (r'^geturl/(?P<path>.+)$', views.getUrl),
    (r'^upload/$', views.upload),
    (r'^del/$', views.delete2),
    (r'^del/(?P<path>.+)$', views.delete),
    (r'^dest/$', views.destraction2),
    (r'^dest/(?P<path>.+)$', views.destraction),
    (r'^createdir/$', views.createDir),
    (r'^createdir/(?P<path>.+)$', views.createDir),
    (r'^addbuffer/$', views.addBuffer),
    (r'^past/$', views.past),
    (r'^past/(?P<path>.+)$', views.past),
    (r'^remove/$', views.RemoveFromBuffer),
    (r'^remove/(?P<path>.+)$', views.RemoveFromBuffer),
    (r'^rename/(?P<path>.+)$', views.rename),
    (r'^basket/$', views.listBasket),
    (r'^view/$', views.view),
    (r'^view/(?P<path>.+)$', views.view),
    (r'^image/(?P<path>.+)$', views.image),
    (r'^download/(?P<path>.+)$', views.download),
)
