from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from log import views

urlpatterns = patterns('log',
    # Examples:  
    #url(r'^vmoneylist/$', views.vmoneylist, name='vmoneylist'),
     
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
