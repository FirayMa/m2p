# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import *
from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404,render
import pdb
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
from basedatas.common import Common
comm    = Common()
dmb     = DetectMobileBrowser()

def index(request):
    isMobile = dmb.process_request(request)
     
    if not request.user.is_anonymous():
         heartbeat_list = HeartBeat.objects.filter(owner=request.user).order_by('-pk')
    else:
         heartbeat_list = ''

    context = {'heartbeat_list' : heartbeat_list}
    isMobile = dmb.process_request(request)
     
    if isMobile:
        return render(request, 'heartbeat/m_index.html', context)
    else:
        return render(request, 'heartbeat/m_index.html', context)
     
        
def new(request):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
       return comm.redirect_login_path(isMobile, request)
		
    context = { }
    isMobile = dmb.process_request(request)
    if isMobile:
        return render(request, 'heartbeat/m_new.html', context)
    else:
        return render(request, 'heartbeat/m_new.html', context)
@csrf_exempt    
def save(request):
    if  request.user.is_anonymous():
        return redirect(settings.APP_WEB_LOGIN_URL)
     
    if request.method == 'POST' and 'words' in request.POST:
        words     = request.POST["words"]
         
        heartbeat = HeartBeat.objects.create(words=words,date=timezone.now(),owner=request.user) 
        heartbeat.save()
        return HttpResponse("保存成功...")
      
            
def confirm_delete(request, heartbeat_id):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)


    heartbeat    = get_object_or_404(HeartBeat, pk = heartbeat_id, owner=request.user)
    context = {"heartbeat":heartbeat}
    isMobile = dmb.process_request(request)
    if isMobile:
        return render(request, 'heartbeat/m_delete.html', context)
    else:
        return render(request, 'heartbeat/m_delete.html', context) 
@csrf_exempt
def do_delete(request):
    if  request.user.is_anonymous():
        return redirect(settings.APP_WEB_LOGIN_URL)
		
    if request.POST:
        heartbeat_id = request.POST.get('id')
        heartbeat    = get_object_or_404(HeartBeat, pk = heartbeat_id, owner=request.user)
        heartbeat.delete()
    
        return  HttpResponse("删除成功...")
    else:
        return  HttpResponse("无法删除...")
