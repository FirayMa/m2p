from django.shortcuts import render
from .models import *
from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404,render
import pdb
from django.utils import timezone


from basedatas.bd_comm import Common
from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser

dmb     = DetectMobileBrowser()
comm    = Common()

def index(request):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
        
    bill_list = Bill.objects.filter(user=request.user).order_by('-id')

    context = {'bill_list'          : bill_list}

    
    return render(request, 'bill/index.html', context)
    
	

def new(request):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    
    context = {'page':'new' } 
    return render(request, 'bill/new.html', context)
    
def change(request, bill_id):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    
    bill         = Bill.objects.get(pk = bill_id)
    context = {'bill':bill,
               'page':'change',
               'user': request.user
               }
    
    return render(request, 'bill/new.html', context)    
def save(request):
    if  request.user.is_anonymous():
        return redirect(settings.APP_WEB_LOGIN_URL)
     
    if request.method == 'POST':
        page                 = request.POST["page"]
        type_name            = request.POST["type"]
        flag_name            = request.POST["flag"]
        money_name           = request.POST["money"]
        item_name            = request.POST["item"]
        remark_name          = request.POST["remark"]
        if flag_name == '1':
            flag_bool = True
        else:
            flag_bool = False
        if page == 'new':
            bill = Bill.objects.create(sort=type_name, flag=flag_bool, money=money_name,item=item_name,
             remark=remark_name,date=timezone.now(),user=request.user) 
        
            bill.save()
            return HttpResponse(bill.pk)
        else:
            billid          = request.POST["bill_id"]
            bill = Bill.objects.get(pk = billid)
            bill.flag = flag_bool
            bill.sort = type_name
            bill.money = money_name
            bill.item = item_name
            bill.remark = remark_name
            bill.save()
            return HttpResponse(bill.pk)
