from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from bill import views

urlpatterns = patterns('bill',
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.new, name='new'), #new bill
    url(r'^save/$', views.save, name='save'), #save bill
    url(r'^(?P<bill_id>\d+)/change/$', views.change, name='change'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
