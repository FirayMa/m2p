from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from blocks import views

urlpatterns = patterns('blocks',
    # Examples:  
    url(r'^newblock/$', views.newblock, name='newblock'),
    url(r'^(?P<blockid>\d+)/changeblock/$', views.changeblock, name='changeblock'),
    url(r'^list/$', views.list, name='list'),
    url(r'^community_block_list/$', views.community_block_list, name='community_block_list'),
    url(r'^product_block_list/$', views.product_block_list, name='product_block_list'),
    url(r'^my_block_list/$', views.my_block_list, name='my_block_list'),
    url(r'^admin_block_list/$', views.admin_block_list, name='admin_block_list'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
