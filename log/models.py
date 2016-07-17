# -*- coding: utf-8 -*-

from django.db import models
from administration.models import User


'''
class VMoneyLog(models.Model):
    """
    the record of virtual money.
    increase or decrease
    """
    owner    =  models.ForeignKey( User, db_index = True)
    time     =  models.DateTimeField( auto_now_add=True )
    #description of the action
    desc     =  models.CharField(max_length = 1024)
    #-1, stand for money decreasing, 
    # 1, stand for money increasing 
    type     =  models.SmallIntegerField()
    #how many increase or decrease this time
    num      =  models.SmallIntegerField()
    
 ''' 

class AdminLog(models.Model):
    """
    the record of administrator operations.
    """
    operator =  models.ForeignKey( User, db_index = True)
    time     =  models.DateTimeField( auto_now_add=True )
    #description of the action
    desc     =  models.TextField()
     
    remark   =  models.TextField(u'备注', null =True)

 