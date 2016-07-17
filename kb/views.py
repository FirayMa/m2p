# -*- coding: utf-8 -*-

from django.shortcuts import render
import getpass 
import pdb
from django.utils import timezone
import datetime
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404,render
import os
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
from datetime import datetime


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
from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
from PIL import Image

"""
3 L
""" 
from basedatas.bd_comm import Common
from common.stat import StatComm
from comment.models import Comment
from msg.models import Msg
from msg.msg_comm import MsgComm 
from .form   import UploadImageForm
from log.models import  AdminLog
from good.models import G_kb 
from .models import Article, Slice, Pic, Active_info, Active_user, Kb_Award, Kb_Collect,Book_user, FreeGift_user, FreeGift
from .models import  Kb_Recommend
from administration.models import User, VerifyCode
from blocks.models import Block 

dmb     = DetectMobileBrowser()
comm    = Common()

sys_log = settings.SYS_LOGGING

#the available statuses are 1, 2
KB_AVAILABLE_STATUS = [1, 2]

def kb_list( request, type):
    """
    create article under a block
    """
    isMobile        = dmb.process_request(request)
    check_kb_autor  =  get_perm_check_kb_autor(request.user)
    
    kb_list = Article.objects.filter(status__in = KB_AVAILABLE_STATUS, type = type).order_by('-is_essence','-dt_set_essence','-date')
    
    
    context = {
                'type'    : type,
                'kb_list' : kb_list,
                'check_kb_autor' : check_kb_autor,
                }
                
    if isMobile:
        return render(request, 'kb/m_kblist.html', context)
    else:
        return render(request, 'kb/m_kblist.html', context)
     
     
def get_perm_check_kb_autor(user):
     '''
     does the user has permission check_kb_autor
     if has, return True
     else return Flase
     '''
     if user.is_anonymous():
         check_kb_autor =  False
     else:  
         check_kb_autor =  user.has_perm('Article.check_kb_autor')
      
      
     return check_kb_autor
     
     
     
def kb_detail( request, kbid):
    """
    create article under a block
    """
    isMobile = dmb.process_request(request)

    try: 
        kb            = Article.objects.get(pk = kbid)
        kb.count_read = kb.count_read + 1
        kb.save()
        
        slice_ls = Slice.objects.filter(article = kb).order_by('num')
       
        pic_ls = Pic.objects.filter(slices__in = slice_ls).order_by('pk')
        if not request.user.is_anonymous():
            is_say_good  = G_kb.objects.filter(owner = request.user, app = kb).count()
            is_collected = Kb_Collect.objects.filter(user = request.user, kb = kb).count()
        else:
            is_say_good  = 0
            is_collected = 0
            
        check_kb_autor  =  get_perm_check_kb_autor(request.user)
        
        context = { 
                    'kb'          : kb,
                    'slice_ls'    : slice_ls, 
                    'pic_ls'      : pic_ls,
                    'rootmedia'   : settings.MEDIA_URL,
                    'is_say_good' : is_say_good,
                    'is_collected': is_collected,
                    'check_kb_autor' : check_kb_autor,
                   }
        
                
        if isMobile:
            if kb.type == 1 or kb.type == 0:
                return render(request, 'kb/m_detail.html', context)
            if kb.type == 2:
                return render(request, 'kb/m_product_detail.html', context)
            if kb.type == 3:
                return render(request, 'kb/m_product_detail.html', context)
        else:
            if kb.type == 1 or kb.type == 0:
                return render(request, 'kb/m_detail.html', context)
                
            if kb.type == 2:
                return render(request, 'kb/m_product_detail.html', context)
                
            if kb.type == 3:
                return render(request, 'kb/m_product_detail.html', context) 
            
    except Article.DoesNotExist: 
        print '[error]', str(kbid), 'Article.DoesNotExist exception'
        return HttpResponse(u'未找到帖子..')
    except Article.MultipleObjectsReturned:
        print '[error]', str(kbid), 'Article.MultipleObjectsReturned exception'
        return HttpResponse(u'找到多个相同帖子..')



def newkb( request):
    """
    create article under a block
    """
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
        
        
    type = 0 #wedding kb
    context = {
                    'page'  : 'new',
                    'type'  : type, 
    }
    if isMobile:
        return render(request, 'kb/m_newkb.html', context)
    else:
        return render(request, 'kb/m_newkb.html', context)
   


def new_speak_wall_kb(request):
    """
    create speak wall kb
    #type == 1
    """
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
        
     
    type = 1 #speak wall kb
    context = {
        'type'    : type,         
    }
    if isMobile:
        return render(request, 'kb/m_newkb.html', context)
    else:
        return render(request, 'kb/m_newkb.html', context)
  


@csrf_exempt
def savekb( request):
    """
    create article under a block
    """ 
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
         
    result = {} 
    if request.method == 'POST': 
        slice_counter     = request.POST['slice_count'] 
        title             = request.POST['title'] 
        kbinstace         = request.POST['kbinstace']
        
        int_slice_counter = int(slice_counter)
        #get block instance  
        if kbinstace == '0':
            #create kb first 
            type              = request.POST['type']
            kb = Article(author = request.user, title=title, desc='..', date=timezone.now(), type= type) 
            kb.save() 
        else: 
        
            kb = Article.objects.get(pk =  kbinstace) 
            kb.title = title
        #change the kb status to 1, stand for this kb has been published.    
        kb.status = 1
        kb.save() 
        
      
        #start to save slice for this article
        #how many slices this article have? : int_slice_counter
        for i in range(1, int_slice_counter+1):
            #get slice instace
            kb_slice_instace_name      = 'kb_slice_instace_'+ str(i)#this is the slice instance name in html
            article_content_name       = 'article_content_' + str(i)#this is the slice content name in html 
            #get slice instance
            
            kb_slice_instace_id = request.POST[kb_slice_instace_name]
            article_content     = request.POST[article_content_name] 
            if kb_slice_instace_id == '0': 
                slice_instance = Slice(article = kb, content = article_content, num=i)
            else:
                slice_instance = Slice.objects.get(pk =  kb_slice_instace_id)
                slice_instance.content = article_content
                slice_instance.num     = i
          
            slice_instance.save()

        
        result['status'] = 'OK'
        result['id']     = kb.id
    else:
        print '[Error][save_kb] request method error'
        result['status'] = 'ERROR'
        result['msg']    = '1 can not find the picture'

    return HttpResponse(json.dumps(result), content_type='application/json')
 

@csrf_exempt
def upload_image(request):
    """
    upload the article image
    """ 
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    result = {}
    if request.method == 'POST':
	form = UploadImageForm(request.POST, request.FILES) 
      
	if form.is_valid(): 
	    usesr = request.user
	    
	    code     = ''.join(random.choice(string.lowercase + string.digits) for i in range(10))
	    filename = handle_uploaded_image(request.FILES['imagefile'], str(usesr.id)+'_'+ code)
	     
            id_kb       = request.POST['id_kb']
            id_kb_slice = request.POST['id_kb_slice']
      
            if id_kb == '0':
                #create kb first
                 
                kb = Article(author = request.user, title='...', desc='..', date=timezone.now())
                kb.save() 
            else: 
                kb = Article.objects.get(pk =  id_kb)
       
            if id_kb_slice == '0': 
                slice_instance = Slice(article = kb, content = '...')
                slice_instance.save()
            else:
                slice_instance = Slice.objects.get(pk =  id_kb_slice)
   
            pic_instance = Pic(slices = slice_instance, link = filename.replace('\\', '/'), uploader= request.user)
            pic_instance.save()
     

	    result['status']  = 'OK'
	    result['msg']     = '上传成功...'
	    
	    result['file']    = os.path.join(settings.MEDIA_URL, filename)
	    
	    result['id_kb']           = kb.id
	    result['id_kb_slice']     = slice_instance.id
	    result['id_pic']          = pic_instance.id
	    
	else:
            result['status'] = 'ERROR'
	    result['msg']    = '请先选择图片..'
             
    else:
	result['status'] = 'ERROR'
	result['msg']    = '请先选择图片..'
  
    return HttpResponse(json.dumps(result), content_type='application/json')

def handle_uploaded_image(f, userid):
	filename = str(userid) + '_'+ timezone.now().strftime('%Y%m%d%H%M%S%f')+ '.jpg' 
 
	upload_dir = os.path.join(settings.MEDIA_ROOT, 'kb')
	if not os.path.isdir(upload_dir):
            os.makedirs(upload_dir)
	with open(os.path.join(settings.MEDIA_ROOT, 'kb', filename), 'wb+') as destination: 
	    for chunk in f.chunks() :
		destination.write(chunk)
		
	if os.path.getsize(destination.name) > settings.FILE_MAX_SIZE :
            image = Image.open(destination.name) 
            image.save(destination.name,quality=settings.FILE_COMPRESSION_RIO,optimize=True)
	
	return os.path.join('kb', filename)

@csrf_exempt
def del_pic( request ):
    """
    delete a picture via ID

    , picid
    
    """
    result = {}
    try:
        picid = request.POST['picid']
        pic_instance = Pic.objects.get(pk = picid)
        pic_url = os.path.join(settings.MEDIA_ROOT, pic_instance.link.name)
        
        #delete picture file
        if os.path.isfile(pic_url):
            os.remove(pic_url)
            
        pic_instance.delete()
        result['status'] = 'OK'
        result['msg']    = 'OK'
         
    except Pic.DoesNotExist:
        print '[Error] can not find the picture', picid
        result['status'] = 'ERROR'
        result['msg']    = 'can not find the picture'

    return HttpResponse(json.dumps(result), content_type='application/json')


   
def my_kb_list(request, blockid):
    """
    get all kbs which author is current user
    """
     
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
        
    
    kb_list = Article.objects.filter(block__id = blockid, status__in = KB_AVAILABLE_STATUS, author =  request.user).order_by('-is_essence','-dt_set_essence', '-date')
        
    context = { 
                'kb_list' : kb_list,
              }
    if isMobile:
        return render(request, 'kb/m_my_kblist.html', context)
    else:
        return render(request, 'kb/m_my_kblist.html', context)
    
def all_my_kb_list(request):
    """
    get all kbs which author is current user
    """
     
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
        
    
    kb_list = Article.objects.filter( status__in = KB_AVAILABLE_STATUS, author =  request.user).order_by('block', '-is_essence','-dt_set_essence', '-date')
        
    context = { 
                'kb_list' : kb_list,
              }
    if isMobile:
        return render(request, 'kb/m_my_kblist.html', context)
    else:
        return render(request, 'kb/m_my_kblist.html', context)

def all_kb_list(request, blockid):
    """
    get all kbs for administrator
    """
     
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    user = request.user
    manage_perm = user.has_perm('kb.manage_all_kb')
    kb_list = Article.objects.filter(block__id = blockid, status__in = KB_AVAILABLE_STATUS ).order_by('-is_essence','-dt_set_essence', '-date')
        
    context = { 
                'kb_list' : kb_list,
                'manage_perm' : manage_perm,
              }
    if isMobile:
        return render(request, 'kb/m_all_kblist.html', context)
    else:
        return render(request, 'kb/m_all_kblist.html', context)

def set_kb_top_pic(request, kbid ):
    """
    after article has been published successfully, user select to set top picture
    """
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
        
    user = request.user
    has_perm = user.has_perm('kb.can_modify_all_kb_top_pic')
     
    try:
        kb = Article.objects.get(pk = kbid)
        if user == kb.author :
            has_own_perm = True 
        else:
            has_own_perm = False 
    except Article.DoesNotExist:
        kb            = ''
        has_perm     = False
        has_own_perm = False
           
    context = { 
                'kb'       : kb,
                'has_perm' : has_perm,
                'rootmedia': settings.MEDIA_URL,
                'has_own_perm':has_own_perm,
              }
    if isMobile:
        return render(request, 'kb/m_toppic.html', context)
    else:
        return render(request, 'kb/m_toppic.html', context)


@csrf_exempt       
def good_add( request):
    result = {}
    if request.method == 'POST':
        kbid = request.POST['kbid']
        try:  
            kb      = Article.objects.get(pk = kbid)
            
            kb.count_good = kb.count_good+ 1 
            kb.save()
            result['status']  = 'OK'
            result['good_count']     = kb.count_good,
                
       
            
        except Article.DoesNotExist:
            sys_log.error('Article.DoesNotExist exception. ID is %s ',str( kbid)) 
            result['status'] = 'ERROR'
            result['msg']    = 'Article.DoesNotExist' 
        except Article.MultipleObjectsReturned:
            sys_log.error('Article.MultipleObjectsReturned exception. ID is %s ',str( kbid))
            result['status'] = 'ERROR'
            result['msg']    = 'Article.MultipleObjectsReturned'  
    return HttpResponse(json.dumps(result), content_type='application/json')    


@csrf_exempt
def save_kb_top_pic(request):
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    result = {}
    if request.method == 'POST':
	form = UploadImageForm(request.POST, request.FILES) 
	if form.is_valid(): 
	    usesr = request.user
	    
	    code     = ''.join(random.choice(string.lowercase + string.digits) for i in range(10))
	    filename = handle_uploaded_image(request.FILES['imagefile'], str(usesr.id)+'_'+ code)
	     
            id_kb       = request.POST['id_kb']

            kb = Article.objects.get(pk =  id_kb)
            kb.top_pic = filename.replace('\\', '/')
            kb.save()
            #pic_instance = Pic(slices = slice_instance, link = filename.replace('\\', '/'), uploader= request.user)
            #pic_instance.save()

	    result['status']  = 'OK'
	    result['msg']     = '上传成功...' 
	    result['id_kb']   = kb.id 
	    
	else:
            sys_log.warning('form invalide.')
            result['status'] = 'ERROR'
	    result['msg']    = '请先选择图片..'
             
    else:
        sys_log.warning('request method error.')
	result['status'] = 'ERROR'
	result['msg']    = '请先选择图片..'
  
    return HttpResponse(json.dumps(result), content_type='application/json')



def changekb(request, kbid):
    """
    """
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    user = request.user
    #administrator can modify all kb
    
    try:  
        kb      = Article.objects.get(pk = kbid)
        if request.user == kb.author:
            perm  = True    # only can modify their own kb
        else:
            perm  = False
     

        context = {'kb'     : kb,
                    'perm'   : perm,
                    'rootmedia': settings.MEDIA_URL,
        }
        
    except Article.DoesNotExist:
        sys_log.error('Article.DoesNotExist exception. ID is %s ',str( kbid)) 
        return HttpResponse(u'未找到板块..')
    except Article.MultipleObjectsReturned:
        sys_log.error('Article.MultipleObjectsReturned exception. ID is %s ',str( kbid))
        return HttpResponse(u'找到多个相同板块..')
    
    if isMobile:
            if kb.type == 1 or kb.type == 0:
                return render(request, 'kb/m_changekb.html', context)
            if kb.type == 2:
                return render(request, 'kb/m_change_product_kb.html', context)
            if kb.type == 3:
                return render(request, 'kb/m_change_product_kb.html', context)
    else:
            if kb.type == 1 or kb.type == 0:
                return render(request, 'kb/m_changekb.html', context)
                
            if kb.type == 2:
                return render(request, 'kb/m_change_product_kb.html', context)
                
            if kb.type == 3:
                return render(request, 'kb/m_change_product_kb.html', context)    
  

@csrf_exempt
def takepart_in(request):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    result = {} 
    if request.method == 'POST' and 'kbid' in request.POST: 
        user = request.user
        kbid  = request.POST['kbid'] 
        try:  
            kb      = Article.objects.get(pk = kbid)  
            active_user_instance = Active_user(kb = kb, user=user)
            active_user_instance.save()  
            result['status']  = 'OK'
            result['msg']     = '报名成功..'
        except Article.DoesNotExist:
            sys_log.error('Article.DoesNotExist exception. ID is %s ',str( kbid)) 
            result['status']  = 'ERROR'
            result['msg']     = 'Article.DoesNotExist exception' 
        except Article.MultipleObjectsReturned:
            sys_log.error('Article.MultipleObjectsReturned exception. ID is %s ',str( kbid))
            result['status']  = 'ERROR'
            result['msg']     = 'Article.MultipleObjectsReturned exception'  
    else:
        sys_log.warning('request method error.')
	result['status'] = 'ERROR'
	result['msg']    = '参数错误..'
  
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def delkb( request, kbid ):
    """
    delete kb from user list
    """
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    result = {}    
    user = request.user
    perm = user.has_perm('kb.manage_all_kb')
    if perm:
        try: 
            kb        = Article.objects.get(pk = kbid)
            kb.status = 3 #delete the kb
            kb.save()
 
            title = '这是帖子标题'
            descrip = '管理员删除帖子, 帖子ID：%d', kb.id, '帖子标题为:%s ', kb.title
            admin_log_instance = AdminLog(operator = user, desc = descrip)
            admin_log_instance.save()
            result['status'] = 'OK'
            result['msg']    = '删除成功..'
        except Article.DoesNotExist:
            sys_log.error('Article.DoesNotExist exception. ID is %s ',str( kbid)) 
            result['status']  = 'ERROR'
            result['msg']     = 'Article.DoesNotExist exception' 
        except Article.MultipleObjectsReturned:
            sys_log.error('Article.MultipleObjectsReturned exception. ID is %s ',str( kbid))
            result['status']  = 'ERROR'
            result['msg']     = 'Article.MultipleObjectsReturned exception' 
    else:
        result['status'] = 'ERROR'
        result['msg']    = '权限错误..'
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def best_kb( request, kbid ):
    """
    set kb to be essence kb
    """
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    result = {}    
    user = request.user
    perm = user.has_perm('kb.manage_all_kb')
    if perm:
        try: 
            kb            = Article.objects.get(pk = kbid)
            kb.is_essence = 1
            kb.dt_set_essence = timezone.now()
            kb.save()
 
            title = '这是帖子标题'
            descrip = '管理员设置帖子为精华帖, 帖子ID：%d', kb.id, '帖子标题为:%s ', kb.title
            admin_log_instance = AdminLog(operator = user, desc = descrip)
            admin_log_instance.save()
            
            #section for sliver 
            reach_top = MoneyComm.reachEsseceKbTopMoney(kb.author) 
            if not reach_top: 
                 MoneyComm.awardEssenceKb(kb.author, kb)
            
            result['status'] = 'OK'
            result['msg']    = '设置成功..'
        except Article.DoesNotExist:
            sys_log.error('Article.DoesNotExist exception. ID is %s ',str( kbid)) 
            result['status']  = 'ERROR'
            result['msg']     = 'Article.DoesNotExist exception' 
        except Article.MultipleObjectsReturned:
            sys_log.error('Article.MultipleObjectsReturned exception. ID is %s ',str( kbid))
            result['status']  = 'ERROR'
            result['msg']     = 'Article.MultipleObjectsReturned exception' 
    else:
        result['status'] = 'ERROR'
        result['msg']    = '权限错误..'
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def cancel_best_kb( request, kbid ):
    """
    #cancel to set kb to be essence
    """
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    result = {}    
    user = request.user
    perm = user.has_perm('kb.manage_all_kb')
    if perm:
        try: 
            kb            = Article.objects.get(pk = kbid)
            kb.is_essence = 0 #cancel to set kb to be essence
            kb.dt_set_essence = None
            kb.save()
 
            title = '这是帖子标题'
            descrip = '管理员%s取消帖子为精华帖, 帖子ID：%d', user.name, kb.id, '帖子标题为:%s ', kb.title
            admin_log_instance = AdminLog(operator = user, desc = descrip)
            admin_log_instance.save()
            result['status'] = 'OK'
            result['msg']    = '设置成功..'
        except Article.DoesNotExist:
            sys_log.error('Article.DoesNotExist exception. ID is %s ',str( kbid)) 
            result['status']  = 'ERROR'
            result['msg']     = 'Article.DoesNotExist exception' 
        except Article.MultipleObjectsReturned:
            sys_log.error('Article.MultipleObjectsReturned exception. ID is %s ',str( kbid))
            result['status']  = 'ERROR'
            result['msg']     = 'Article.MultipleObjectsReturned exception' 
    else:
        result['status'] = 'ERROR'
        result['msg']    = '权限错误..'
    return HttpResponse(json.dumps(result), content_type='application/json')

@csrf_exempt
def award_kb( request ):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    result = {}  
    if request.method == 'POST' and 'kbid' in request.POST and 'silver' in request.POST: 
        user = request.user
        kbid    = request.POST['kbid']
        silver  = int(request.POST['silver'])
        
        if silver > user.v_silver:
            result['status']  = 'ERROR'
            result['msg']     = '没有足够的仓库币...'
        else:
            
            if silver > settings.TOP_AWARD_V_M:
                result['status']  = 'ERROR'
                result['msg']     = '打赏仓库币最多不能超过:%d'%settings.TOP_AWARD_V_M
            else:
                try:  
                    kb      = Article.objects.get(pk = kbid)
                    if user == kb.author:
                        result['status']  = 'ERROR'
                        result['msg']     = '不能给自己打赏'
                    else:
                        kb_award_ls = Kb_Award.objects.filter(user = user, kb = kb)
                        total_silver_award = 0
                        for kb_award in kb_award_ls:
                            total_silver_award = total_silver_award + kb_award.money
                        if total_silver_award + silver > settings.TOP_AWARD_V_M:
                            result['status']  = 'ERROR'
                            result['msg']     = '超过单篇帖子打赏限额，最多还可以打赏:%d..'% (total_silver_award-settings.TOP_AWARD_V_M)
                        else:
                            #
                            vmoney_list = Vmoney_detail.objects.filter(user = user, mark = 1).order_by('-date_in')
                            if vmoney_list:
                                 total_silver_award = 0
                                 for vmoney in vmoney_list:
                                     total_silver_award = total_silver_award + vmoney.money 
                                     if total_silver_award >= silver:
                                          if  total_silver_award == silver:
                                               vmoney.mark     = -1
                                               vmoney.type_out = 0
                                               vmoney.date_out = timezone.now()
                                               vmoney.save()
                                          else:
                                               vmoney.money = total_silver_award - silver
                                               vmoney.save()
                                          
                                          break
                            #reduce the silver from the request.user
                            user.v_silver = user.v_silver - silver
                            user.save()
                            
                            #increase the gold for the KB author
                            kb.author.v_gold  += silver
                            kb.author.save()
                            
                            
                            
                            kb_award_instance = Kb_Award(user = user, kb = kb, money= silver)
                            kb_award_instance.save()
                            
                            #start to add new msg to msg app
                            #call msg app to add msg item to DB
                            msg_url = reverse('kb:kb_detail', args={ kb.id})  
                            msgtext = u'%s打赏了你的帖子..'%(user.get_full_name())
                            urlpic = '' 
                            type = 3 # from award kb
                            MsgComm.add(kb.author, msg_url, urlpic, msgtext, type, user)

                            vmoney_gold = Vmoney_detail(user = kb.author, type_in = 6, url=msg_url,  money = silver, desc=u'帖子打赏获得金币', value=0 )
                            vmoney_gold.save()
                            
                            vmoney_record = Vmoney_detail(user = user, type_in = 7,  mark =0, url=msg_url, money = silver, desc=u'帖子打赏消费银币' )
                            vmoney_record.save()
                            
                            #increase the gold for the KB author
                            kb.author.msg_mark  = True
                            kb.author.save()
                            
                            result['status']  = 'OK'
                            result['msg']     = '谢谢打赏..'
                except Article.DoesNotExist:
                    sys_log.error('Article.DoesNotExist exception. ID is %s ',str( kbid)) 
                    result['status']  = 'ERROR'
                    result['msg']     = 'Article.DoesNotExist exception' 
                except Article.MultipleObjectsReturned:
                    sys_log.error('Article.MultipleObjectsReturned exception. ID is %s ',str( kbid))
                    result['status']  = 'ERROR'
                    result['msg']     = 'Article.MultipleObjectsReturned exception'  
    else:
        sys_log.warning('request method error.')

    return HttpResponse(json.dumps(result), content_type='application/json')


def award_userlist( request, kbid):
    isMobile = dmb.process_request(request) 
     
    user = request.user  
    try: 
        kb  = Article.objects.get(pk = kbid)
        kb_award_list = Kb_Award.objects.filter(kb = kb).order_by('-date')
        context = {'kb_award_list': kb_award_list,}
    except Article.DoesNotExist:
        sys_log.error('Article.DoesNotExist exception. ID is %s ',str( kbid))  
    except Article.MultipleObjectsReturned:
        sys_log.error('Article.MultipleObjectsReturned exception. ID is %s ',str( kbid)) 
   
    if isMobile:
        return render(request, 'kb/m_userlist.html', context)
    else:
        return render(request, 'kb/m_userlist.html', context)
    
def active_userlist( request, kbid):
    isMobile = dmb.process_request(request) 
     
    user = request.user
    perm = user.has_perm('kb.manage_all_kb')
    
    try: 
        kb  = Article.objects.get(pk = kbid)
        if user == kb.author:
            perm = True
            
        active_user_list = Active_user.objects.filter(kb = kb).order_by('-date')
        context = {
                   'active_user_list': active_user_list,
                   'perm'            :  perm
                   }
        
    except Article.DoesNotExist:
        sys_log.error('Article.DoesNotExist exception. ID is %s ',str( kbid))   
    except Article.MultipleObjectsReturned:
        sys_log.error('Article.MultipleObjectsReturned exception. ID is %s ',str( kbid))  
    if isMobile:
        return render(request, 'kb/m_active_userlist.html', context)
    else:
        return render(request, 'kb/m_active_userlist.html', context)
    

@csrf_exempt
def collect_kb( request ):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        result['status']  = '1'
        result['msg']     = '请先登录...'
    else: 
        result = {}  
        if request.method == 'POST' and 'kbid' in request.POST : 
            try:
                kbid    = request.POST['kbid'] 
                kb  = Article.objects.get(pk = kbid) 
                try:
                    Kb_Collect.objects.get(kb = kb, user = request.user)
                except Kb_Collect.DoesNotExist:
                    kb_collect_instance = Kb_Collect(kb = kb, user = request.user)    
                    kb_collect_instance.save()
                except Kb_Collect.MultipleObjectsReturned:
                    kb_collect_list = Kb_Collect.objects.get(kb = kb, user = request.user)
                    for kb_collect in kb_collect_list:
                        kb_collect.delete()
                    kb_collect_instance = Kb_Collect(kb = kb, user = request.user)    
                    kb_collect_instance.save()
                     
                result['status']  = 'OK'
                result['msg']     = '收藏成功...'
                
            except Article.DoesNotExist:
                sys_log.error('Article.DoesNotExist exception. ID is %s ',str( kbid))  
                result['status']  = 'ERROR'
                result['msg']     = 'Article.DoesNotExist exception'
            except Article.MultipleObjectsReturned:
                sys_log.error('Article.MultipleObjectsReturned exception. ID is %s ',str( kbid))
                result['status']  = 'ERROR'
                result['msg']     = 'Article.MultipleObjectsReturned exception' 
        else:
            sys_log.warning('request method error.')
          
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def collect_del_kb( request ):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        result['status']  = '1'
        result['msg']     = '请先登录...'
    else:
        result = {}  
        if request.method == 'POST' and 'kbid' in request.POST : 
            try:
                kbid    = request.POST['kbid'] 
                kb  = Article.objects.get(pk = kbid) 
                try:
                    kb_collect_instance = Kb_Collect.objects.get(kb = kb, user = request.user)
                    kb_collect_instance.delete()
                except Kb_Collect.DoesNotExist:
                    pass
                except Kb_Collect.MultipleObjectsReturned:
                    kb_collect_list = Kb_Collect.objects.get(kb = kb, user = request.user)
                    for kb_collect in kb_collect_list:
                        kb_collect.delete() 
                     
                result['status']  = 'OK'
                result['msg']     = '已取消收藏...'
                
            except Article.DoesNotExist:
                sys_log.error('Article.DoesNotExist exception. ID is %s ',str( kbid))  
                result['status']  = 'ERROR'
                result['msg']     = 'Article.DoesNotExist exception'
            except Article.MultipleObjectsReturned:
                sys_log.error('Article.MultipleObjectsReturned exception. ID is %s ',str( kbid))
                result['status']  = 'ERROR'
                result['msg']     = 'Article.MultipleObjectsReturned exception' 
        else:
            sys_log.warning('request method error.')
          
    return HttpResponse(json.dumps(result), content_type='application/json')

def collect_list( request):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    
    user = request.user 
    
    try: 
        collect_list = Kb_Collect.objects.filter(user = user).order_by('-date')
        context = {
                   'collect_list': collect_list, 
                   }
        
    except Article.DoesNotExist:
        sys_log.error('Article.DoesNotExist exception. ID is %s ',str( kbid))   
    except Article.MultipleObjectsReturned:
        sys_log.error('Article.MultipleObjectsReturned exception. ID is %s ',str( kbid))  
    if isMobile:
        return render(request, 'kb/m_kb_collect_list.html', context)
    else:
        return render(request, 'kb/m_kb_collect_list.html', context)


def new_product_kb(request, blockid):
    """
    create new product article under a block
    #type == 2
    """
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
        
    try:  
        block_instance = Block.objects.get(pk = blockid)
        type = 2 #new product kb
        context = {
            'blockid' : blockid, 
            'type'    : type,         
        }
        if isMobile:
            return render(request, 'kb/m_new_free_product_kb.html', context)
        else:
            return render(request, 'kb/m_new_free_product_kb.html', context)
    except Block.DoesNotExist:
        print '[error]', str(blockid), 'Block.DoesNotExist exception'
        return HttpResponse(u'未找到板块..')
    except Block.MultipleObjectsReturned:
        print '[error]', str(blockid), 'Block.MultipleObjectsReturned exception'
        return HttpResponse(u'找到多个相同板块..')


def new_gift_kb(request, blockid):
    """
    create new gift article under a block
    #type == 3
    """
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
        
    try:  
        block_instance = Block.objects.get(pk = blockid)
        type = 3 #new gift kb
        context = {
            'blockid' : blockid, 
            'type'    : type,         
        }
        if isMobile:
            return render(request, 'kb/m_new_free_product_kb.html', context)
        else:
            return render(request, 'kb/m_new_free_product_kb.html', context)
    except Block.DoesNotExist:
        print '[error]', str(blockid), 'Block.DoesNotExist exception'
        return HttpResponse(u'未找到板块..')
    except Block.MultipleObjectsReturned:
        print '[error]', str(blockid), 'Block.MultipleObjectsReturned exception'
        return HttpResponse(u'找到多个相同板块..')
        
        
@csrf_exempt
def book_new_product(request):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    result = {} 
    if request.method == 'POST' and 'kbid' in request.POST: 
        user = request.user
        kbid  = request.POST['kbid'] 
        try:  
            kb      = Article.objects.get(pk = kbid)
            try:
                book_instance = Book_user.objects.get(kb = kb, user=user)
                result['status']  = 'ERROR'
                result['msg']     = '你已预约过了...' 
            except Book_user.DoesNotExist: 
                book_user_instance = Book_user(kb = kb, user=user)
                book_user_instance.save()
                need_money = kb.money
                #
                vmoney_list = Vmoney_detail.objects.filter(user = user, mark = 1).order_by('-date_in')
                if vmoney_list:
                     total_silver_award = 0
                     for vmoney in vmoney_list:
                         total_silver_award = total_silver_award + vmoney.money 
                         if total_silver_award >= need_money:
                              if  total_silver_award == need_money:
                                   vmoney.mark     = -1
                                   vmoney.type_out = 1 #book new product
                                   vmoney.date_out = timezone.now()
                                   vmoney.save()
                              else:
                                   vmoney.money = total_silver_award - need_money
                                   vmoney.save()
                              
                              break
                            
                user.v_silver = user.v_silver - need_money
                user.save()
                
                result['status']  = 'OK'
                result['msg']     = '预约成功..'
        except Article.DoesNotExist:
            sys_log.error('Article.DoesNotExist exception. ID is %s ',str( kbid)) 
            result['status']  = 'ERROR'
            result['msg']     = 'Article.DoesNotExist exception' 
        except Article.MultipleObjectsReturned:
            sys_log.error('Article.MultipleObjectsReturned exception. ID is %s ',str( kbid))
            result['status']  = 'ERROR'
            result['msg']     = 'Article.MultipleObjectsReturned exception'  
    else:
        sys_log.warning('request method error.')
	result['status'] = 'ERROR'
	result['msg']    = '参数错误..'
  
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def recieve_gift(request):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    result = {} 
    if request.method == 'POST' and 'kbid' in request.POST: 
        user = request.user
        kbid  = request.POST['kbid'] 
        try:  
            kb      = Article.objects.get(pk = kbid)
            try:
                freegift = FreeGift.objects.get(kb = kb) 
                if freegift.min_level > user.level: 
                    result['status']  = 'ERROR'
                    result['msg']     = '你的会员等级不够...' 
                else: 
                    try: 
                        gift_instance = FreeGift_user.objects.get(kb = kb, user=user) 
                        result['status']  = 'ERROR'
                        result['msg']     = '你已预领取过了...' 
                    except FreeGift_user.DoesNotExist:  
                        gift_instance = FreeGift_user(kb = kb, user=user)
                        gift_instance.save() 
                        freegift.number =   freegift.number-1
                        freegift.save()
                        result['status']  = 'OK'
                        result['msg']     = '领取成功..'
            except FreeGift.DoesNotExist: 
                result['status']  = 'ERROR'
                result['msg']     = 'FreeGift.DoesNotExist exception' 
            
        except Article.DoesNotExist:
            sys_log.error('Article.DoesNotExist exception. ID is %s ',str( kbid)) 
            result['status']  = 'ERROR'
            result['msg']     = 'Article.DoesNotExist exception' 
        except Article.MultipleObjectsReturned:
            sys_log.error('Article.MultipleObjectsReturned exception. ID is %s ',str( kbid))
            result['status']  = 'ERROR'
            result['msg']     = 'Article.MultipleObjectsReturned exception'  
    else:
        sys_log.warning('request method error.')
	result['status'] = 'ERROR'
	result['msg']    = '参数错误..'
  
    return HttpResponse(json.dumps(result), content_type='application/json')

def book_userlist(request, kbid):
    isMobile = dmb.process_request(request) 
     
    user = request.user  
    try: 
        kb  = Article.objects.get(pk = kbid)
        kb_book_list = Book_user.objects.filter(kb = kb).order_by('-date')
        context = {'kb_book_list': kb_book_list,}
    except Article.DoesNotExist:
        sys_log.error('Article.DoesNotExist exception. ID is %s ',str( kbid))  
    except Article.MultipleObjectsReturned:
        sys_log.error('Article.MultipleObjectsReturned exception. ID is %s ',str( kbid)) 
   
    if isMobile:
        return render(request, 'kb/m_book_userlist.html', context)
    else:
        return render(request, 'kb/m_book_userlist.html', context)


def freegift_userlist(request, kbid):
    isMobile = dmb.process_request(request) 
     
    user = request.user  
    try: 
        kb  = Article.objects.get(pk = kbid)
        kb_free_gift_list = FreeGift_user.objects.filter(kb = kb).order_by('-date')
        context = {'kb_free_gift_list': kb_free_gift_list,}
    except Article.DoesNotExist:
        sys_log.error('Article.DoesNotExist exception. ID is %s ',str( kbid))  
    except Article.MultipleObjectsReturned:
        sys_log.error('Article.MultipleObjectsReturned exception. ID is %s ',str( kbid)) 
   
    if isMobile:
        return render(request, 'kb/m_free_gift_userlist.html', context)
    else:
        return render(request, 'kb/m_free_gift_userlist.html', context)
        
def my_freegift(request):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
        
    #type = 3 free gift
    kb_list = Article.objects.filter(type = 3, status__in = KB_AVAILABLE_STATUS, freegift_user__user = request.user).order_by('-is_essence','-dt_set_essence', '-date')
        
    context = { 
                'kb_list' : kb_list,
              }
    if isMobile:
        return render(request, 'kb/m_my_kblist.html', context)
    else:
        return render(request, 'kb/m_my_kblist.html', context)
        
        
def my_book(request):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
        
    #type = 3 book product
    kb_list = Article.objects.filter(type = 2, status__in = KB_AVAILABLE_STATUS, book_user__user = request.user).order_by('-is_essence','-dt_set_essence', '-date')
        
    context = { 
                'kb_list' : kb_list,
              }
    if isMobile:
        return render(request, 'kb/m_my_kblist.html', context)
    else:
        return render(request, 'kb/m_my_kblist.html', context)


@csrf_exempt       
def recommend_to_block( request, kbid):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    
    return recommend(request, kbid, 0)
    


@csrf_exempt       
def recommend_to_homepage_slice( request, kbid):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    
    return recommend(request, kbid, 1)


def recommend(request, kbid, type):
    '''
    type = 0 recommend to block slice
    type = 1 recommend to homepage slice
    type = 2 recommend to homepage kb list
    '''
    result = {}    
    user = request.user
    perm = user.has_perm('kb.manage_all_kb')
    if perm:
        try: 
            kb            = Article.objects.get(pk = kbid)
            try:
                if type == 0:
                     kb_recommend = Kb_Recommend.objects.get(kb = kb ,  type_block='1')
                
                if type == 1:
                     kb_recommend = Kb_Recommend.objects.get(kb = kb ,  type_homepage_slice='1') 
                     
                if type == 2:
                     kb_recommend = Kb_Recommend.objects.get(kb = kb,  type_homepage_kb='1') 
                     
                     
                result['status'] = 'ERROR'
                result['msg']    = '已经被推荐, 不需要再次推荐..'
            except Kb_Recommend.DoesNotExist:
                if type == 0:
                    kb_recommend = Kb_Recommend(kb = kb,  type_block='1')
                    
                if type == 1:
                    kb_recommend = Kb_Recommend(kb = kb,  type_homepage_slice='1')
                    
                if type == 2:
                    kb_recommend = Kb_Recommend(kb = kb,  type_homepage_kb='1')
                    
                kb_recommend.save()
                
                title = '这是帖子标题'
                descrip = '管理员推荐帖子至板块轮播图, 帖子ID：%d', kb.id, '帖子标题为:%s ', kb.title
                admin_log_instance = AdminLog(operator = user, desc = descrip)
                admin_log_instance.save()
                """
                #section for sliver 
                reach_top = MoneyComm.reachEsseceKbTopMoney(kb.author) 
                if not reach_top: 
                    MoneyComm.awardEssenceKb(kb.author, kb)
                """
                result['status'] = 'OK'
                result['msg']    = '设置成功..'
        except Article.DoesNotExist:
            sys_log.error('Article.DoesNotExist exception. ID is %s ',str( kbid)) 
            result['status']  = 'ERROR'
            result['msg']     = 'Article.DoesNotExist exception' 
        except Article.MultipleObjectsReturned:
            sys_log.error('Article.MultipleObjectsReturned exception. ID is %s ',str( kbid))
            result['status']  = 'ERROR'
            result['msg']     = 'Article.MultipleObjectsReturned exception' 
    else:
        result['status'] = 'ERROR'
        result['msg']    = '权限错误..'
    return HttpResponse(json.dumps(result), content_type='application/json')
    
    
    
def search( request):
    context = {}
    kb_list  = '' 
    if request.method == 'GET':
        if 'keywords' in request.GET: 
            keywords      = request.GET['keywords'] 
            keywords_list = keywords.split(' ') 
            query         = reduce(lambda x, y: x|y, [Q(title__icontains = keyword) for keyword in keywords_list])
            kb_list        = Article.objects.filter(query, status__in = KB_AVAILABLE_STATUS).order_by('-date')
           
    context = {
        'kb_list': kb_list,
    }
    return render(request, 'kb/m_search_kblist.html', context)
