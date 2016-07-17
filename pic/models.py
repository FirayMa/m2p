# -*- coding: utf-8 -*-


from django.db import models
from administration.models import User
from django.utils import timezone


# the models for the Picture
class Pic( models.Model ):
	#url structure:
	#                top
	#    userid1            userid2
	#pic1 pic2 pic3   pic1 pic2 pic3 pic4
	url = models.CharField(max_length = 1024)
	#the creator
	user = models.ForeignKey(User)
	#modified date
	date = models.DateTimeField(auto_now = True)
	#title of this message
	title = models.CharField(max_length = 1000, default=' ')
	
	description         = models.TextField('描述', default=' ')
	is_saved     		= models.BooleanField(u'是否保存了上传后的图片',default=False)