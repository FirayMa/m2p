# -*- coding: utf-8 -*-

from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from django.shortcuts import redirect
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404

import pdb
import json

from .models import LastInfo,L_Receiver,Tofuture

from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
from basedatas.bd_comm import Common
from common.stat import StatComm


comm    = Common()
#instance for detecting mobile or desktop device.
dmb     = DetectMobileBrowser()

def index_lastinfo(request):
        StatComm.count_page_traffic(request)
        isMobile = dmb.process_request(request)
        if  request.user.is_anonymous():
                lastinfo_list = ''
        else:
                lastinfo_list = LastInfo.objects.filter(user =  request.user).order_by('-date')
        context = {'lastinfo_list':lastinfo_list}
        if isMobile:
             return render(request, 'lastinfo/m_index.html', context )
        else:
             return render(request, 'lastinfo/index.html', context )   

def new_lastinfo(request):
        StatComm.count_page_traffic(request)
        is_Mobile = dmb.process_request(request)
        if  request.user.is_anonymous():
                return comm.redirect_login_path(is_Mobile, request)
        context = {'page':'new'}
        if is_Mobile:
                return render(request, 'lastinfo/m_new.html', context )
        else:                
                return render(request, 'lastinfo/new.html', context )

def change_lastinfo(request,lastinfo_id):
        StatComm.count_page_traffic(request)
        isMobile = dmb.process_request(request)
        if  request.user.is_anonymous():
                return comm.redirect_login_path(isMobile, request)
        
        #modify a last info
        try:
                lastinfo_instance = get_object_or_404(LastInfo, id=lastinfo_id, user=request.user)
                lrcv_list = L_Receiver.objects.filter(lastinfo_pk = lastinfo_instance)
                context = {'lastinfo':lastinfo_instance,
                           'lrcv_list':lrcv_list,
                           'page':'change'}
                
                if isMobile:
                     return render(request, 'lastinfo/m_new.html', context )
                else:                
                     return render(request, 'lastinfo/new.html', context ) 
        except Http404:
                return HttpResponseNotFound('<h1>Page not found</h1>')
        



def detail_lastinfo(request, id_lastinfo ):
        StatComm.count_page_traffic(request)
        isMobile = dmb.process_request(request)
        if  request.user.is_anonymous():
                return comm.redirect_login_path(isMobile, request)

        try:
                lastinfo_instance = get_object_or_404(LastInfo, id=id_lastinfo, user=request.user)
               
                context = {'lastinfo':lastinfo_instance}
                return render(request, 'lastinfo/detail.html', context )
        except Http404:
                return HttpResponseNotFound('<h1>Page not found</h1>')
         

@csrf_exempt
def save_lastinfo(request):
        StatComm.count_page_traffic(request)
        #save the changes for last info
        if  request.user.is_anonymous():
                return redirect(settings.APP_WEB_LOGIN_URL)
        
        result = {}
        
        if request.method == 'POST':
                if 'title' in request.POST and 'recipients' in request.POST and 'days' in request.POST and 'content' in request.POST :
                        
                        title           = request.POST.get('title')
                        recipients      = request.POST.get('recipients')
                        days            = request.POST.get('days')
                        content         = request.POST.get('content')
                        page            = request.POST.get('page')
                        

                        content         = content.encode('utf8','ignore')
                        title           = title.encode('utf8','ignore')
                             
                        if recipients:
                                list_recipient = recipients.split(',')
                                
                                #save last mail instance
                                if page == 'new':
                                        last_info_instance = LastInfo.objects.create(title=title, days=days, mgs=content, user= request.user) 
                                        last_info_instance.save()
                                else:
                                        id              = request.POST.get('id')
                                        
                                        try:
                                                last_info_instance = LastInfo.objects.get(id = id, user = request.user)
                                                last_info_instance.title   = title
                                                last_info_instance.days    = days
                                                last_info_instance.mgs     = content
                                                last_info_instance.is_sent = '0'
                                                last_info_instance.save()
                                        except LastInfo.DoesNotExist:
                                                 result['status'] = 'ERROR'                                     
                                                 result['MSG']    = '要修改的记录不存在...'
                                                 return HttpResponse(json.dumps(result), content_type='application/json')

                                        l_rcvs = L_Receiver.objects.filter(lastinfo_pk=last_info_instance)
                                        for l_rcv in l_rcvs:
                                                l_rcv.delete()
                                 
                                for recipient in list_recipient:   
                                        l_rcv = L_Receiver.objects.create(email=recipient, lastinfo_pk=last_info_instance) 
                                        l_rcv.save()
                                             
                                result['status']        = 'OK'
                                result['id']            = last_info_instance.id
                                result['MSG']           = '已成功提交至服务器...'
                                 
                        else:
                                result['status'] = 'ERROR'                                     
                                result['MSG']    = '嘿嘿，你还是不对,不过我已经给你提示了...'
                                
                        
                else:
                        result['status'] = 'ERROR'
                        result['MSG']    = '嘿嘿，就不告诉你...'
                        
        else:
                result['status'] = 'ERROR'
                result['MSG'] = '嘿嘿，气死你...'
                
        return HttpResponse(json.dumps(result), content_type='application/json')


def new_tofuture(request):
        StatComm.count_page_traffic(request)
        is_Mobile = dmb.process_request(request)
        
        context = {'page':'new'}
        if is_Mobile:
                return render(request, 'tofuture/m_new.html', context )
        else:                
                return render(request, 'tofuture/new.html', context )


def change_tofuture(request,tofuture_id):
        StatComm.count_page_traffic(request)
        isMobile = dmb.process_request(request)
        if  request.user.is_anonymous():
                return comm.redirect_login_path(isMobile, request)
        
        #modify a last info
        try:
                tofuture_instance = get_object_or_404(Tofuture, id=tofuture_id, user=request.user)
                
                context = {'tofuture_instance':tofuture_instance,
                           'page':'change'}
                
                if isMobile:
                     return render(request, 'tofuture/m_new.html', context )
                else:                
                     return render(request, 'tofuture/m_new.html', context ) 
        except Http404:
                return HttpResponseNotFound('<h1>Page not found</h1>')


@csrf_exempt
def save_tofuture(request):
        StatComm.count_page_traffic(request)
        #save the changes for last info
        if  request.user.is_anonymous():
                return redirect(settings.APP_WEB_LOGIN_URL)
        
        result = {}
        if request.method == 'POST':
                if 'title' in request.POST and 'years' in request.POST and 'content' in request.POST :
                        
                        title           = request.POST.get('title')
                        years           = request.POST.get('years')
                        content         = request.POST.get('content')
                        page            = request.POST.get('page') 

                        content         = content.encode('utf8','ignore')
                        title           = title.encode('utf8','ignore')
                         
                        #save last mail instance
                        if page == 'new':
                               
                                tofuture_instance = Tofuture.objects.create(title=title, years=years, mgs=content, user= request.user) 
                                tofuture_instance.save()
                        else:
                                id      = request.POST.get('id')
                                
                                try:
                                        tofuture_instance = Tofuture.objects.get(id = id, user = request.user)
                                        tofuture_instance.title         = title
                                        tofuture_instance.years         = years
                                        tofuture_instance.mgs           = content
                                        tofuture_instance.save()
                                except Tofuture.DoesNotExist:
                                         result['status'] = 'ERROR'                                     
                                         result['MSG']    = '要修改的记录不存在...'
                                         return HttpResponse(json.dumps(result), content_type='application/json')
                        result['status']        = 'OK'
                        result['id']            = tofuture_instance.id
                        result['MSG']           = '已成功提交至服务器...' 
                else:
                        result['status'] = 'ERROR'
                        result['MSG']    = '嘿嘿，就不告诉你...'
                        
        else:
                result['status'] = 'ERROR'
                result['MSG'] = '嘿嘿，气死你...'
                
        return HttpResponse(json.dumps(result), content_type='application/json')


def detail_tofuture(request, tofuture_id ):
        StatComm.count_page_traffic(request)
        isMobile = dmb.process_request(request)
        if  request.user.is_anonymous():
                return comm.redirect_login_path(isMobile, request)

        try:
                tofuture_instance = get_object_or_404(Tofuture, id=tofuture_id, user=request.user)
                context = {'tofuture':tofuture_instance}
                return render(request, 'tofuture/detail.html', context )
        except Http404:
                return HttpResponseNotFound('<h1>Page not found</h1>')


def index_tofuture(request):
        StatComm.count_page_traffic(request)
        isMobile = dmb.process_request(request)
        if  request.user.is_anonymous():
                return comm.redirect_login_path(isMobile, request)
        
        tofuture_list = Tofuture.objects.all()
        context = {'tofuture_list':tofuture_list}

        return render(request, 'tofuture/index.html', context )
