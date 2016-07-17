# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.http import Http404
from django import forms
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
import shutil
from django.contrib.admin import AdminSite
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from administration.models import User
from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
import pdb

"""
layer 2 start
"""
from django.contrib.auth import logout

"""
layer 2 end
"""





from basedatas.bd_comm import Common

dmb     = DetectMobileBrowser()
comm    = Common()

def home(request):
    
    isMble  = dmb.process_request(request)
    context = {}
    if isMble: 
        return HttpResponse('M login Page')
        #return render(request, 'map2family/m_hostpage.html', context)
    else: 
        return HttpResponse('PC login Page')
        #return render(request, 'admin/login.html', context)

def logout_view(request):
    logout(request)
    isMble  = dmb.process_request(request)
    context = {  }
    if isMble:
        return render(request, 'map2family/m_logout.html', context)
    else:
        return render(request, 'map2family/logout.html', context)

@csrf_exempt    
def login(request):
  
    isMble  = dmb.process_request(request)
    
    if 'email' in request.POST and 'password' in request.POST:
            auth.logout(request)
            u_email       = request.POST['email']
            password      = request.POST['password']
            user = auth.authenticate(email=u_email, password=password)
            next_url = request.POST.get('next')
            context ={}
            if user:
                # User is valid.  Set request.user and persist user in the session
                # by logging the user in.
                request.user = user
                auth.login(request, user)
                # redirect to the value of next if it is entered, otherwise
		# to settings.APP_WEB_PC_LOGIN_URL
		 
		if next_url:
                    #after login, return to the previous page, but if the previous page is logout, 
                    #then return to the host page
                    if 'logout' not in str(next_url):
                         return redirect(next_url)
                
                if isMble:
                        return render(request, 'map2family/m_hostpage.html', context)
                else:
                        return render(request, 'map2family/hostpage.html', context)
            else:
                try:
                    user_instance = User.objects.get(email = u_email)
                    msg = '登录失败，密码错误...'
                except User.DoesNotExist:
                    msg = '登录失败，用户未注册...'
                    
                context = {'next':next_url,
                           'error':msg,
                           'email':u_email}
                if isMble: 
			return render(request, 'registration/m_login.html', context)
		else:  
			return render(request, 'registration/login.html', context)
		    
    else:
                next_url = request.GET.get('next')
                email = request.POST.get('email')
		context = {'next':next_url,
                           'error':'',
                           'email':email}

		if isMble: 
			return render(request, 'registration/m_login.html', context)
		else:  
			return render(request, 'registration/login.html', context)
			
			
'''
@csrf_exempt
def m_login(request):
    if 'email' in request.POST and 'password' in request.POST:
        auth.logout(request)
        u_email       = request.POST['email']
        password    = request.POST['password']
        user = auth.authenticate(email=u_email, password=password)
        if user:
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in.
            request.user = user
            auth.login(request, user)
            return redirect(request.POST.get('next',settings.APP_WEB_HOST_URL))
            #return redirect(settings.APP_WEB_HOST_URL)
        else:
            context = {'error':'登录失败，用户不存在或者密码错误.'}
            return render(request, 'registration/m_login.html', context)
             
    else:
        return HttpResponse('not in')
'''   
class MyAdminSite(AdminSite):
    @never_cache
    def index(self, request, extra_context=None):
         context = {}
         return render(request, 'mapfamily/index.html', context)
