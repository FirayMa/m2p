from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from ticket import views

urlpatterns = patterns('ticket',
    url(r'^$', views.index, name='index'),
    url(r'^openTicket/$', views.open_ticket, name='openTicket'), #new  Ticket
    url(r'^saveticket/$', views.save_ticket, name='saveticket'), #
    url(r'^(?P<ticket_id>\d+)/detail/$', views.detail, name='detail'),
    url(r'^(?P<ticket_id>\d+)/change/$', views.change_ticket, name='change'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
