# -*- coding: utf-8 -*-


import smtplib
from email import encoders
from email import Utils
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart  
from email.MIMEText import MIMEText
import pdb

SMTP_SERVER_USER = 'postmaster@map2family.com'
SMTP_SERVER_PWD  = 'Youxiang889886'
SMTP_SERVER      = 'smtp.mxhichina.com'

class EmailEx(object):
    def send_text_email(self,Subject,content,receiver,user_email):
         
            sender              = 'postmaster@map2family.com'
            themsg              = MIMEMultipart()
            themsg['Subject']   = Subject
            themsg['To']        = receiver
            themsg['From']      = 'map2family'
            themsg['Date']      = Utils.formatdate(localtime = 1)
            themsg['Message-ID'] = Utils.make_msgid()
            msgAlternative      = MIMEMultipart('alternative')
            themsg.attach(msgAlternative)
            content = '---此邮件由map2family代'+user_email+'发送。<br/>' + content + '<br/>-----www.map2family.com'
            msgText = MIMEText(content,'html', 'utf-8')
            msgAlternative.attach(msgText)
            themsgtest = themsg.as_string()      
            # send the message
            server = smtplib.SMTP()  
            server.connect(SMTP_SERVER) 
            server.login(SMTP_SERVER_USER, SMTP_SERVER_PWD)
            server.sendmail(sender, receiver, themsgtest)
            server.quit()#SMTP.quit()
            
