# -*- coding: utf-8 -*-

from django.db import models
from administration.models import User

class Block( models.Model):
    """
    the blocks for forum
    every article will belongs to one block
    """
    creator   =  models.ForeignKey(User)
    date      =  models.DateTimeField( )
    
    title     =  models.CharField(u'板块名称', max_length = 1024)
    #description of the action
    desc      =  models.TextField(u'板块简介', max_length = 1024, default ='')
    #the count of article in this block
    num       =  models.IntegerField(u'主题', default = 0)
    #the default value is 1, stand for that this block is ready to user
    #if the block is deleted, this will be set to 0, not available for any users, but not really deleted from DB
    status    =  models.SmallIntegerField(u'删除', default = 1)
    
    
    COMMUNITY   = 0
    PRODUCT     = 1
    BLOCK_CHOICES = (
        (COMMUNITY, u'社区'),
        (PRODUCT, u'产品'), 
    )
    type             = models.SmallIntegerField(u'板块归属',
                                      choices=BLOCK_CHOICES,
                                      default=COMMUNITY) 
 
    
    class Meta:
            permissions = (
                ("block_management", "管理板块:创建，修改"),
            )
            
            
