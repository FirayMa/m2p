# -*- coding: utf-8 -*- 

 
from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404,render
import pdb 
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

'''
layer 3 start
'''
from .models import Todo_list
from .form import Todo_listForm
from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
from basedatas.bd_comm import Common
'''
layer 3 end
'''


dmb     = DetectMobileBrowser()
comm    = Common()


'''
TODO list section  START
'''

def todolist(request):
    '''
    list all TODO
    '''
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request) 
        
    has_perm = request.user.has_perm('task.manage_todolist')
    
    if has_perm:
        todo_ls = Todo_list.objects.all().order_by('-date')
    else:# permission denied
        todo_ls = ''
        
    context = {'has_perm': has_perm,
               'todo_ls' : todo_ls  }
    if isMobile:
        return render(request, 'task/m_todolist.html', context)
    else:
        return render(request, 'task/m_todolist.html', context)


'''
TODO list section  END
'''


def  deltest(request):
     return render(request, 'task/test.html', {}) 

@csrf_exempt
def  add(request):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    
    
    user = request.user
    if  not user.has_perm('administration.admin_management'):
        context = {
                     'not_granted' : True, 
                  }
    else:
        try: 
            if request.method == 'POST':
                form = Todo_listForm(request.POST) 
                if form.is_valid(): 
                     
                    new_todo_job             = form.save(commit=False)
                    new_todo_job.date        = timezone.now()
                    new_todo_job.publisher   = user
                    new_todo_job.save()
                    
                    context = { 
                         'form'       :  form,
                         'saved'      :  True,
                         'validate'   :  True,
                      }
                else:
                    #invalide form
                    form = Todo_listForm()
                    context = {
                         'form'       : form,
                         'validate'   : False,
                      }
            else: 
                form = Todo_listForm()
                context = {
                         'form'       : form,
                         'validate'   :  True,
                      }
        except Todo_list.DoesNotExist:
            context = {
                         'usernotexist'   :  True,
                      }
        
    
    if isMobile:    
        return render(request, 'task/m_todo.html', context)
    else:
        return render(request, 'task/m_todo.html', context)
