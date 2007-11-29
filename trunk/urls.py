from django.conf.urls.defaults import *
from fileman import views
import fileman.settings as settings

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^list/$', views.list),
    (r'^list/(?P<path>.+)/$', views.list),
    (r'^preview/(?P<path>.+)$', views.preview),
    (r'^geturl/(?P<path>.+)$', views.getUrl),
    (r'^upload/$', views.upload),
    (r'^del/$', views.delete),
    (r'^dest/$', views.destraction),
    (r'^createdir/(?P<path>.+)$', views.createDir),
    (r'^addbuffer/$', views.addBuffer),
    (r'^past/(?P<path>.+)$', views.past),
    (r'^remove/(?P<path>.+)$', views.RemoveFromBuffer),
    (r'^basket/$', views.listBasket),
)