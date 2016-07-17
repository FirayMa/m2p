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

from .models import Pic

from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser

from basedatas.bd_comm import Common
from common.stat import StatComm

comm    = Common()
#instance for detecting mobile or desktop device.
dmb     = DetectMobileBrowser()


def index(request):
        StatComm.count_page_traffic(request)
        isMobile = dmb.process_request(request)
        #if  request.user.is_anonymous():
        #       return comm.redirect_login_path(isMobile, request)
        
        #pic_list = Pic.objects.filter(user=request.user).order_by('-pk')
        #context = {'pic_list':pic_list}
        context = {}
        if isMobile:
            return render(request, 'pic/m_index.html', context )
        else:
            return render(request, 'pic/index.html', context )

def demo(request):
        StatComm.count_page_traffic(request)
        isMobile = dmb.process_request(request)
        context = {}
        if isMobile:
            return render(request, 'pic/m_demo.html', context )
        else:
            return render(request, 'pic/m_demo.html', context )

def upload(request):
        StatComm.count_page_traffic(request)
        is_Mobile = dmb.process_request(request)
        if  request.user.is_anonymous():
                return comm.redirect_login_path(isMobile, request)
        
        context = {}
        if is_Mobile:
                return render(request, 'pic/m_upload.html', context )
        else:                
                return render(request, 'pic/m_upload.html', context )


def delete(request):
        StatComm.count_page_traffic(request)
        is_Mobile = dmb.process_request(request)
        
        context = {'page':'new'}
        if is_Mobile:
                return render(request, 'lastinfo/m_new.html', context )
        else:                
                return render(request, 'lastinfo/new.html', context )
