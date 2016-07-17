from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from mailer import views

urlpatterns = patterns('mailer',
    #url(r'^$', views.index, name='index'),
    url(r'^index_lastinfo/$', views.index_lastinfo, name='index_lastinfo'),  
    url(r'^new_lastinfo/$', views.new_lastinfo, name='new_lastinfo'), #create a lastinfo
    url(r'^save_lastinfo/$', views.save_lastinfo, name='save_lastinfo'), #save lastinfo
    url(r'^(?P<lastinfo_id>\d+)/change_lastinfo/$', views.change_lastinfo, name='change_lastinfo'),
    url(r'^(?P<id_lastinfo>\d+)/detail_lastinfo/$', views.detail_lastinfo, name='detail_lastinfo'),

    url(r'^new_tofuture/$', views.new_tofuture, name='new_tofuture'), #create an email sent to future
    url(r'^(?P<tofuture_id>\d+)/change_tofuture/$', views.change_tofuture, name='change_tofuture'),
    url(r'^save_tofuture/$', views.save_tofuture, name='save_tofuture'), #save
    url(r'^(?P<tofuture_id>\d+)/detail_tofuture/$', views.detail_tofuture, name='detail_tofuture'),
    url(r'^index_tofuture/$', views.index_tofuture, name='index_tofuture'),  
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
