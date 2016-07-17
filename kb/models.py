# -*- coding: utf-8 -*-

from django.db import models
from administration.models import User
from blocks.models import Block


class Article(models.Model):
    """
    the article for forum
    every article will belongs to one block
    every article may has one or more slices
    """ 
    author    =  models.ForeignKey( User)
    date      =  models.DateTimeField(u'发表日期')
    title     =  models.CharField(u'标题', max_length = 1024)
    #description of the article
    desc      =  models.TextField(u'摘要',  default ='')
    #how many times of this article has been read 
    count_read        =  models.IntegerField(u'阅读', default = 0)
    #how many likes of this article 
    count_good        =  models.IntegerField(u'赞', default = 0)
    #how many times of this article has been replied 
    count_reply       =  models.IntegerField(u'回复', default = 0)
    top_pic           =  models.ImageField(u'顶图',  upload_to='article', null=True)
    #the default value is 0 : draft
    #                     1 : pubished
    #                     2 : best article
    #                     3 : deleted
    #if the article is deleted, this will be set to 3, not available for any users, but not really deleted from DB
    status           =  models.SmallIntegerField(u'状态', default = 0)
    
    #if this value is set to 1, it is a essence kb
    is_essence       =  models.SmallIntegerField(u'精华贴', default = 0)
    dt_set_essence   =  models.DateTimeField(u'设置精华的日期', null=True)
    #the type of kb
    #default 0 is the wedding kb
    #value 1 is the speak wall kb
    #value 2 is the new product kb
    #value 3 is the free gift kb
    type             = models.SmallIntegerField(u'帖子类型', default = 0)
    
    url              = models.TextField(u'商城链接',null = True)
    money            = models.SmallIntegerField(u'仓库币',null = True)
    class Meta:
            permissions = (
                ("cannot_publish_kb", u"黑名单:不能发帖，不能回帖"),  
                ("cannot_modify_kb",  u"修改帖子权限:没有权限修改帖子"),  
                ("can_modify_all_kb_top_pic",  u"可以设置所有帖子的顶图"), 
                ("can_modify_all_kb",  u"管理员可以修改所有人的贴子"),
                ("can_del_all_kb",  u"管理员可以删除所有人的贴子"),  
                ("manage_all_kb",  u"管理贴子：删除，设为精华，设置轮播图."),
                ("check_kb_autor",  u"有查看帖子作者名称."),    
            )


class Slice(models.Model):
    """
    the Slice in Article
    every article will belongs to one block
    every article may has one or more slices
    relationship:
    Block   : Article = 1 : n 
    Article : Slice   = 1 : n 
    """
    article      =  models.ForeignKey( Article)
    #description of the slice
    content      =  models.TextField('',  default ='')
    
    num          =  models.SmallIntegerField('序号',  default =1)
    
class Pic(models.Model):
    """
    the pictures in Slice
    every article will belongs to one block
    every article may has one or more slices
    relationship:
    Block   : Article = 1 : n 
    Article : Slice   = 1 : n 
    Slice   : Pic     = 1 : n 
    """
    slices      =  models.ForeignKey(Slice)
    #description of the slice
    link        =  models.ImageField('',  upload_to='article')	
    uploader    =  models.ForeignKey(User, related_name = 'pic_user')
    #the default value is 0 : draft
    #                     1 : saved
    #if the article is saved, this will be set to 1
    #if the article is draft and the user is leaving the page, the pictures with status=0 should been deleted.
    status      =  models.SmallIntegerField(u'图片状态', default = 0)


class Active_info(models.Model):
    """
    this model is for active kb
    """
    kb          =  models.ForeignKey(Article)
    deadline    =  models.DateField('截止日期')	 
    number      =  models.SmallIntegerField(u'活动上限人数', default = 100)


class FreeGift(models.Model):
    """
    for free gift
    """
    kb          =  models.ForeignKey(Article)
    #deadline    =  models.DateField('截止日期')	 
    number      =  models.SmallIntegerField(u'礼品数量', default = 100)
    min_level   =  models.SmallIntegerField(u'会员等级', default = 0)   


class FreeGift_user(models.Model):
    """
    the users who get the gift
    """
    kb      =  models.ForeignKey(Article)  
    user    =  models.ForeignKey(User)
    date    =  models.DateTimeField(auto_now_add = True, null = True)

class Active_user(models.Model):
    """
    the users who take part in the active
    """
    kb      =  models.ForeignKey(Article)  
    user    =  models.ForeignKey(User)
    date    =  models.DateTimeField(auto_now_add = True, null = True)


class Book_user(models.Model):
    """
    the users who book the new active
    """
    kb      =  models.ForeignKey(Article)  
    user    =  models.ForeignKey(User)
    date    =  models.DateTimeField(auto_now_add = True, null = True)


class Kb_Award(models.Model):
    """
    the users list who award the kb
    """
    kb      =  models.ForeignKey(Article)  
    user    =  models.ForeignKey(User)
    money   =  models.SmallIntegerField(u'打赏金额')
    date    =  models.DateTimeField(auto_now_add = True)
    
class Kb_Collect(models.Model):
    """
    the users kb collection list
    """
    kb      =  models.ForeignKey(Article)  
    user    =  models.ForeignKey(User) 
    date    =  models.DateTimeField(auto_now_add = True)
    
class Kb_Recommend(models.Model):
    """
    the users kb collection list
    """
    kb               =  models.ForeignKey(Article)  
    
    #type_block = 0 this is default value, not be recommnended to block
    #type_block = 1  be recommnended to block silce
    type_block       =  models.CharField('推荐至板块', max_length=10, default='0') 
    
    #type_homepage_slice = 0 this is default value, not be recommnended to homepage
    #type_homepage_slice = 1  be recommnended to homepage silce
    type_homepage_slice    =  models.CharField('推荐至首页轮播图', max_length=10 , default='0') 
    
    #type_homepage_kb = 0 this is default value, not be recommnended to homepage to lisk this kb
    #type_homepage_kb = 1  be recommnended to homepage silce to list kb
    type_homepage_kb       =  models.CharField('推荐至首页帖子列表', max_length=10 , default='0')  
    
    date    =  models.DateTimeField(auto_now_add = True)