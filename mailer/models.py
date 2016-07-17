# -*- coding: utf-8 -*-


from django.db import models
from administration.models import User
from django.utils import timezone

# the models for the last information
class LastInfo( models.Model ):
	#days stand for that this letter will be sent to receivers after these days.
	days = models.IntegerField(default = 100)
	#the main text message
	mgs  = models.BinaryField()
	#the creator
	user = models.ForeignKey(User)
	#modified date
	date = models.DateTimeField(auto_now = True)
	#title of this message
	title = models.CharField(max_length = 500, default='--发自map2family')

	#sent or not
	#default is 0, stand for not sent.
	#1, stand for sent.
	is_sent = models.CharField(max_length = 10, default='0')
	

#who receive the messsage from feature LastInfo	
class L_Receiver( models.Model ):
	email 		= models.EmailField(max_length = 254)
	lastinfo_pk  	= models.ForeignKey(LastInfo)

#this class is for the email sent to themself in the future
class Tofuture( models.Model):
        #years stand for that this letter will be sent to receivers after these days.
	years = models.DecimalField('years', max_digits=5, decimal_places=2, default=2)
	mgs  = models.BinaryField()
	#the creator
	user = models.ForeignKey(User)
	#modified date
	date = models.DateTimeField(auto_now = True)
	#title of this message
	title = models.CharField(max_length = 500, default='--发自map2family')

	#sent or not
	#default is 0, stand for not sent.
	is_sent = models.CharField(max_length = 10, default='0')
	
