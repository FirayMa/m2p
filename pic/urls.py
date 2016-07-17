from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from pic import views

urlpatterns = patterns('pic',
    url(r'^$', views.index, name='index'),
    url(r'^demo/$', views.demo, name='demo'), #beautiful demo picture
    url(r'^upload/$', views.upload, name='upload'), #upload picture
    #url(r'^save/$', views.save, name='save'), #save item
    #url(r'^(?P<heartbeat_id>\d+)/confirm_delete/$', views.confirm_delete, name='confirm_delete'),
    url(r'^delete/$', views.delete, name='delete'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
