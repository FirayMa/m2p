# -*- coding: utf-8 -*-

from django.db import models
#from django.contrib.auth.models import User
from administration.models import User
# Create your models here.
class Ticket(models.Model):
    creator         = models.ForeignKey(User, verbose_name='username')
    title           = models.CharField(u'标题',max_length=1000)
    comments        = models.TextField(u'详细说明')
    createDate_date = models.DateTimeField('create date')
    #'0' stand for not finished; '1' stand for finished
    isFinished      = models.CharField('is finished',max_length=1, default='0')
    class Meta:
            permissions = (
                #allocate this permission to our customer
                #can close the ticket opened by himeself
                ("close_ticket", "允许关闭ticket权限."),
                #allocate this permission to dev group
                #can see all ticket
                ("dev_ticket", "开发组管理ticket."),
            )