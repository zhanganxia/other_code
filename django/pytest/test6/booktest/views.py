# from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
# from django.views.generic import View

def send(request):
    msg='<a href="http://www.itcast.cn/subject/pythonzly/index.shtml" target="_blank">点击激活</a>'
    send_mail('注册激活','',settings.DEFAULT_FROM_EMAIL,
              ['605613403@qq.com'],
              html_message=msg)
    return HttpResponse('ok')
# class MyView(View):
#     def get(self,request,*args,**kwargs):
#         return HttpResponse('Hello,world!')

# Create your views here.
# 创建session_set和session_get视图如下（测试redis存储session）
# def session_set(request):
#     request.session['name'] = 'zax'
#     return HttpResponse('ok')

# def session_get(request):
#     name = request.session['name']
#     return HttpResponse(name)



