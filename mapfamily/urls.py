from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sites.models import Site
from mapfamily import views

urlpatterns = patterns('',
    url(r'^bill/', include('bill.urls', namespace="bill")),
    url(r'^heartbeat/', include('heartbeat.urls', namespace="heartbeat")),
    url(r'^user/', include('administration.urls', namespace="user")),
    url(r'^ticket/', include('ticket.urls', namespace="ticket")),
    url(r'^base/', include('basedatas.urls', namespace="base")), 
    url(r'^$', 'basedatas.views.index'),
    url(r'^statistics/', include('statistics.urls', namespace="statistics")),
    url(r'^mailer/',include('mailer.urls',namespace='mailer')),
    url(r'^login/',views.login, name='login'),
    url(r'^logout/',views.logout_view, name='logout'),
    url(r'^comment/',include('comment.urls',namespace='comment')),
    url(r'^pic/',include('pic.urls',namespace='pic')),
    url(r'^good/',include('good.urls',namespace='good')),
    url(r'^task/',include('task.urls',namespace='task')), 
    url(r'^msg/',include('msg.urls',namespace='msg')), 
    url(r'^kb/',include('kb.urls',namespace='kb')), 
    url(r'^blocks/',include('blocks.urls',namespace='blocks')),
    #url(r'^m_login/',views.m_login, name='m_login'),
)

urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT ) 
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT ) 

