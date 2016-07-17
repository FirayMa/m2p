# -*- coding: utf-8 -*-
from django.db import models

from administration.models import User
from basedatas.models import Day_words
from kb.models import Article
from django.utils import timezone


# stay praise for day words
class G_daywords(models.Model):
     owner = models.ForeignKey(User)
     app   = models.ForeignKey(Day_words)
     
     
# stay praise for every kb
class G_kb(models.Model):
     owner = models.ForeignKey(User)
     app   = models.ForeignKey(Article)

	
