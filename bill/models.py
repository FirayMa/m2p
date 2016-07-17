# -*- coding: utf-8 -*-
from django.db import models
from administration.models import User
from django.utils import timezone

class Bill(models.Model):
    
    sort    = models.CharField( u'类型',max_length=200, default=u'淘宝')#
    #income or outcome
    #default is income True
    #outcome is false
    flag    = models.BooleanField( u'收支',default=False)#
    money   = models.FloatField( u'金额',default='0.00')
    item    = models.CharField( u'说明',max_length=500,default=u'')
    remark  = models.CharField(u'备注', max_length=2000, default=u'')
    date    = models.DateField(default='1980-01-01')
    user    = models.ForeignKey(User,  blank=True, verbose_name='Creator', null=True)
    

    REQUIRED_FIELDS = ['flag', 'money', 'item']

    def get_money(self):
        
        return self.money

    #def __str__(self):              # __unicode__ on Python 2
    #    return self.email


    def get_item(self):
        # The user is identified by their email address
        return self.item
    
    @property
    def is_flag(self):
        # Simplest possible answer: All admins are staff
        return self.flag
