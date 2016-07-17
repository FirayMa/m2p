from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from kb import views

urlpatterns = patterns('kb',
    url(r'^newkb/$', views.newkb, name='newkb'),
    url(r'^(?P<type>\d+)/kb_list/$', views.kb_list, name='kb_list'),
    url(r'^(?P<kbid>\d+)/kb_detail/$', views.kb_detail, name='kb_detail'), 
    url(r'^(?P<blockid>\d+)/my_kb_list/$', views.my_kb_list, name='my_kb_list'),
    url(r'^(?P<blockid>\d+)/all_kb_list/$', views.all_kb_list, name='all_kb_list'),
    url(r'^upload_image/$', views.upload_image, name='upload_image'),
    
    url(r'^del_pic/$', views.del_pic, name='del_pic'),
    url(r'^savekb/$', views.savekb, name='savekb'),
    url(r'^(?P<kbid>\d+)/set_kb_top_pic/$', views.set_kb_top_pic, name='set_kb_top_pic'), 
    url(r'^save_kb_top_pic/$', views.save_kb_top_pic, name='save_kb_top_pic'),
    url(r'^(?P<kbid>\d+)/changekb/$', views.changekb, name='changekb'),
    
    url(r'^new_speak_wall_kb/$', views.new_speak_wall_kb, name='new_speak_wall_kb'),
    url(r'^takepart_in/$', views.takepart_in, name='takepart_in'),
    url(r'^(?P<kbid>\d+)/delkb/$', views.delkb, name='delkb'),
    url(r'^(?P<kbid>\d+)/best_kb/$', views.best_kb, name='best_kb'),
    url(r'^(?P<kbid>\d+)/cancel_best_kb/$', views.cancel_best_kb, name='cancel_best_kb'),
    
    url(r'^award_kb/$', views.award_kb, name='award_kb'),
    url(r'^(?P<kbid>\d+)/award_userlist/$', views.award_userlist, name='award_userlist'),  
    url(r'^(?P<kbid>\d+)/active_userlist/$', views.active_userlist, name='active_userlist'), #
    url(r'^collect_kb/$', views.collect_kb, name='collect_kb'),
    url(r'^collect_list/$', views.collect_list, name='collect_list'), #
    
    url(r'^collect_del_kb/$', views.collect_del_kb, name='collect_del_kb'),
    url(r'^(?P<blockid>\d+)/new_product_kb/$', views.new_product_kb, name='new_product_kb'),#
    url(r'^book_new_product/$', views.book_new_product, name='book_new_product'),
    url(r'^(?P<kbid>\d+)/book_userlist/$', views.book_userlist, name='book_userlist'), 
    url(r'^(?P<blockid>\d+)/new_gift_kb/$', views.new_gift_kb, name='new_gift_kb'),## 
    
    url(r'^recieve_gift/$', views.recieve_gift, name='recieve_gift'),
    url(r'^(?P<kbid>\d+)/freegift_userlist/$', views.freegift_userlist, name='freegift_userlist'),
    url(r'^my_freegift/$', views.my_freegift, name='my_freegift'),
    url(r'^my_book/$', views.my_book, name='my_book'),
    url(r'^all_my_kb_list/$', views.all_my_kb_list, name='all_my_kb_list'),
    
    url(r'^(?P<kbid>\d+)/recommend_to_block/$', views.recommend_to_block, name='recommend_to_block'),#
    url(r'^(?P<kbid>\d+)/recommend_to_homepage_slice/$', views.recommend_to_homepage_slice, name='recommend_to_homepage_slice'),
    url(r'^search/$', views.search, name='search'),
    url(r'^good_add/$', views.good_add, name='good_add'),#
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
