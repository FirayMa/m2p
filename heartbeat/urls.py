from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from heartbeat import views

urlpatterns = patterns('heartbeat',
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.new, name='new'), #new item
    url(r'^save/$', views.save, name='save'), #save item
    url(r'^(?P<heartbeat_id>\d+)/confirm_delete/$', views.confirm_delete, name='confirm_delete'),
    url(r'^do_delete/$', views.do_delete, name='do_delete'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
