from django.shortcuts import render
import getpass 
from administration.models import User 
 
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

from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser

dmb     = DetectMobileBrowser()

"""
def vmoneylist(request ): 
    if  request.user.is_anonymous():
        return redirect(settings.APP_WEB_LOGIN_URL)
        
    is_Mobile = dmb.process_request(request)
    vmoneyls = VMoneyLog.objects.filter(owner = request.user).order_by('-time')
    
    if is_Mobile:
         return render(request, 'log/m_vmlist.html', {'vmoneyls' : vmoneyls } )
    else:                
         return render(request, 'log/m_vmlist.html', {'vmoneyls' : vmoneyls} )
"""