# -*- coding: utf-8 -*-
from django.db import models
from administration.models import User
from comment.models import Comment
from django import forms
      
"""
class Comment(models.Model):
    content        = models.TextField('comment')
    type           = models.CharField('type',max_length=1)
    commenter      = models.ForeignKey(User, verbose_name='commenter')
    Comment_date   = models.DateTimeField('comment date')
    App_id         = models.IntegerField('app id')
    Commenter_type = models.CharField('Commenter type',max_length=1, default='0')
""" 
class Day_words(models.Model):
    """
    the best words User recommended.
    """
    
    content       = models.TextField('每日精选:')
    #the creator
    user          = models.ForeignKey(User)
    #modified date
    date          = models.DateTimeField(auto_now_add = True)
    good_count    = models.IntegerField('count for praise',default=0)
    comment_count = models.IntegerField('count for comment',default=0)


class Reltn_dayword_comm(models.Model):
    """
    the relationship between Comment and Day_words:
    relationship Day_words: Comment = 1:n
    """
    
    #the instance of Model Day_words
    day_word = models.ForeignKey(Day_words)
    #the instance of Model Comment
    comment = models.ForeignKey(Comment)