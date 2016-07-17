# -*- coding: utf-8 -*-
from django.shortcuts import render
from ticket.models import Ticket
#from django.contrib.auth.models import User
from administration.models import User
from .Form import TicketForm
import pdb
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render

import smtplib
from email import encoders
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart  
from email.MIMEText import MIMEText
from basedatas.e_mail import EmailEx

from django.conf import settings

from django.shortcuts import redirect


from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser


from basedatas.bd_comm import Common
from common.stat import StatComm


dmb     = DetectMobileBrowser()
comm    = Common()


def index(request):
    if  request.user.is_anonymous():
        return redirect(settings.APP_WEB_LOGIN_URL)
    user = request.user
    if user.has_perm('Ticket.dev_ticket'):
        ticket_list = Ticket.objects.all().order_by('isFinished','-createDate_date')
    else:
        ticket_list = Ticket.objects.filter(creator = request.user).order_by('isFinished','-createDate_date')

    has_permission  = user.has_perm('Ticket.close_ticket')
     
    finished_num        = ticket_list.filter(isFinished__exact ='1').count()
    context = {'ticket_list'        : ticket_list
                ,'has_permission'   :has_permission
                ,'finished_num'     :finished_num
    }
    is_Mobile = dmb.process_request(request)
    if is_Mobile:
          return render(request, 'Ticket/m_index.html', context )
    else:                
          return render(request, 'Ticket/index.html', context )
    
def open_ticket(request):
    if  request.user.is_anonymous():
        return redirect(settings.APP_WEB_LOGIN_URL)
    
    try:
        user = User.objects.get(email=request.user.email)
    except:
        HttpResponse('Please Login first !') 
    form = TicketForm()

    page = 'new'
    context = {'form':form,'page':page} 
    is_Mobile = dmb.process_request(request)
    if is_Mobile:
          return render(request, 'Ticket/m_new.html', context )
    else:                
          return render(request, 'Ticket/new.html', context )
 
def change_ticket(request, ticket_id):
    if  request.user.is_anonymous():
        return redirect(settings.APP_WEB_LOGIN_URL)
    
    try:
        user            = User.objects.get(email=request.user.email)
        has_permission  = user.has_perm('Ticket.close_ticket')
    except:
        has_permission  = False
    
    
    ticket = get_object_or_404(Ticket, id=ticket_id)  
    page = 'change'
    form = TicketForm(instance=ticket)
    context = {'form':form
                ,'page':page
                ,'ticket':ticket
                ,'ticket_id':ticket_id
                ,'has_permission':has_permission}
    is_Mobile = dmb.process_request(request)
    if is_Mobile:
          return render(request, 'Ticket/m_new.html', context )
    else:                
          return render(request, 'Ticket/new.html', context )
          
    
def save_ticket(request):
    if  request.user.is_anonymous():
        return redirect(settings.APP_WEB_LOGIN_URL)
    
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            page = request.POST.get('page') 
            if page == 'new':
                new_ticket = form.save(commit=False)
                if request.user.email:
                    creator = request.user.email
                else :
                    return HttpResponse('Please login first!') 
                new_ticket.creator = User.objects.get(email=creator)
                new_ticket.createDate_date = timezone.now()
                new_ticket.save()
                try:
                    Subject   = 'A new Ticket #'+str(new_ticket.id)+' has been opened'
                    receiver  = settings.SUPPORTOR_EMAIL#recipients
                    
                    msgText   = '<h3>'+new_ticket.title +'</h3>' + new_ticket.comments+'<br/> see more detail here:<br/>' +\
                                settings.APP_WEB_URL + 'ticket/' + str(new_ticket.id)+'/detail/'
                    email_intance = EmailEx()
                    email_intance.send_text_email(Subject,msgText,receiver)
                except:
                    print 'send email failed'
                    
                return HttpResponse(u"Ticket 号是: " + str(new_ticket.id)) 
            else:
                ticketid    = request.POST.get('ticketid') 
                ticket = get_object_or_404(Ticket, id=ticketid) 
                change_ticket_form = TicketForm(request.POST, instance=ticket)
                change_ticket_form.save()
                isFinished = request.POST.get('isFinished') 
                if isFinished == 'true':
                    ticket.isFinished = '1'
                else:
                    ticket.isFinished = '0'#re-opened
                    
                ticket.save()
                
                if isFinished == 'true' and ticket.creator.email:
                    #send email to notification the creator
                    try:
                        Subject   = 'The Ticket #'+str(ticket.id)+' you opened has been marked as finished'
                        receiver  = ticket.creator.email#recipients
                        preamble  = 'test'    
                        msgText   = ticket.comments+'\n see more detail here: http://zhaji25-wsgi/ticket/'+\
                                    str(ticket.id)+'/detail/'
                        email_intance = Email()
                        email_intance.send_text_email(Subject,preamble,msgText,receiver)
                    except:
                        pass #send email failed
                    
                return HttpResponse("保存成功!")      
                
        else:
            return HttpResponse("请补全信息...")  
def detail(request, ticket_id):
    if  request.user.is_anonymous():
        return redirect(settings.APP_WEB_LOGIN_URL)
    
    ticket = get_object_or_404(Ticket, id=ticket_id)

    return render(request, 'Ticket/detail.html', {'ticket': ticket})
    
