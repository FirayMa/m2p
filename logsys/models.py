from django.db import models
from django import forms

class log(models.Model):
	app_id	 = models.PositiveIntegerField()	
	location = models.CharField('File Location', max_length=255)
	date	 = models.DateTimeField('Create Date')
	app_type = models.CharField('app type', max_length=1)