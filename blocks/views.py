# -*- coding: utf-8 -*-

from django.shortcuts import render
import getpass 
from administration.models import User, VerifyCode
import pdb
from django.utils import timezone
import datetime
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404,render

from django.views.decorators.csrf import csrf_exempt
import json
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
import random
import string
from django.template import RequestContext, loader
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
import threading

import smtplib
from email import encoders
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart  
from email.MIMEText import MIMEText
from basedatas.e_mail import Email, EmailEx

from django.conf import settings
from django.db.models import Q
import re

from .form import BlockForm
from .models import Block

from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser

dmb     = DetectMobileBrowser()



def newblock( request ): 
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    
    user = request.user
    perm = user.has_perm('blocks.block_management')
    
    if request.method == 'POST':
        form = BlockForm(request.POST) 
        
        if form.is_valid():  
            newblock  =  form.save(commit = False) 
            newblock.creator = user
            newblock.date    = timezone.now()
            newblock.save()
            context = { 
                 'form'       :  form.as_ul(),
                 'saved'      :  True,
                 'validate'   :  True,
              }
        else:
            context = {
                 'form'       : form.as_ul(),
                 'validate'   : False,
              }
    else: 
        form = BlockForm()
        context = {
                 'form'       : form.as_ul(),
                 'validate'   : True,
              }
    context['perm'] = perm
    if isMobile:    
        return render(request, 'blocks/m_new_change_block.html', context)
    else:
        return render(request, 'blocks/m_new_change_block.html', context)


def changeblock(request, blockid ):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    
    user = request.user
    perm = user.has_perm('blocks.block_management')
    block_instance = Block.objects.get(pk = blockid)
    if request.method == 'POST':
        
        form = BlockForm(request.POST, instance = block_instance ) 
        
        if form.is_valid():  
            newblock  =  form.save(commit = False) 
            newblock.creator = user
            newblock.date    = timezone.now()
            newblock.save()
            context = { 
                 'form'       :  form.as_ul(),
                 'saved'      :  True,
                 'validate'   :  True,
              }
        else:
            #invalide form
            form = BlockForm(instance = block_instance)
            context = {
                 'form'       : form.as_ul(),
                 'validate'   : False,
              }
    else: 
        form = BlockForm(instance = block_instance)
        context = {
                 'form'       : form.as_ul(),
                 'validate'   : True,
              }
    context['perm'] = perm
    if isMobile:    
        return render(request, 'blocks/m_new_change_block.html', context)
    else:
        return render(request, 'blocks/m_new_change_block.html', context)
        
        
def list(request):
    isMobile = dmb.process_request(request)

    user = request.user
    perm = user.has_perm('blocks.block_management')

    context = {
                 'perm'       : perm,
              }
              
    if isMobile:    
        return render(request, 'blocks/m_menu.html', context)
    else:
        return render(request, 'blocks/m_menu.html', context)
        
        
def product_block_list(request):
    isMobile = dmb.process_request(request)

    
    user = request.user
    perm = user.has_perm('blocks.block_management')
    
    
    if perm:
        block_ls = Block.objects.filter(type = 1)
    else:
        block_ls = ''
        
    context = {
                 'perm'       : perm,
                 'block_ls'   : block_ls,
              }
              
    if isMobile:    
        return render(request, 'blocks/m_list.html', context)
    else:
        return render(request, 'blocks/m_list.html', context)
        
def community_block_list(request):
    isMobile = dmb.process_request(request)

    
    user = request.user
    perm = user.has_perm('blocks.block_management')
    
    
    if perm:
        block_ls = Block.objects.filter(type = 0)
    else:
        block_ls = ''
        
    context = {
                 'perm'       : perm,
                 'block_ls'   : block_ls,
              }
              
    if isMobile:    
        return render(request, 'blocks/m_list.html', context)
    else:
        return render(request, 'blocks/m_list.html', context)
        
def my_block_list(request):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    user = request.user 
    
    block_ls = Block.objects.filter(type = 0)
   
    context = { 
                 'block_ls'   : block_ls,
              }
              
    if isMobile:    
        return render(request, 'blocks/m_my_list.html', context)
    else:
        return render(request, 'blocks/m_my_list.html', context)
        

def admin_block_list(request):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    
    user = request.user
    perm = user.has_perm('blocks.block_management')
    
    
    if perm:
        block_ls = Block.objects.filter(type = 0)
    else:
        block_ls = ''
        
    context = {
                 'perm'       : perm,
                 'block_ls'   : block_ls,
              }
              
    if isMobile:  
        return render(request, 'blocks/m_admin_list.html', context)
    else:
        return render(request, 'blocks/m_admin_list.html', context)       

def product_block_list(request):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    
    user = request.user
    perm = user.has_perm('blocks.block_management')
    
    
    if perm:
        block_ls = Block.objects.filter(type = 1)
    else:
        block_ls = ''
        
    context = {
                 'perm'       : perm,
                 'block_ls'   : block_ls,
              }
              
    if isMobile:  
        return render(request, 'blocks/m_admin_list.html', context)
    else:
        return render(request, 'blocks/m_admin_list.html', context)       
