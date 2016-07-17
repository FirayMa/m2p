# -*- coding: utf-8 -*-
from django.db import models
from administration.models import User
from django.utils import timezone

class HeartBeat(models.Model):
	owner = models.ForeignKey(User,  blank=True, verbose_name='owner', null=True)
	words = models.CharField(u'写下你想写的', max_length=2000, default=u'')
	
	#auto_now_add
	#Automatically set the field to now when the object is first created.
	#Useful for creation of timestamps. Note that the current date is always used; it’s not just a default value that you can override.
	date  = models.DateTimeField(auto_now_add=True)
