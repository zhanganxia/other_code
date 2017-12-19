from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import View
from user.models import User
import re

# /user/register
class RegisterView(View):
    '''注册'''
    def get(self,request):
        '''显示'''
        return render(request,'register.html')

    def post(self,request):
        '''注册处理'''
        # 接收参数
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        
        # 参数校验
        # 参数完整性校验
        if not all([username,password,email]):
            return render(request,'register.html',{'errmsg':'数据不完整'})
        
        # 校验是否同意协议
        if allow !='on':
            return render(request,'register.html',{'errmsg':'请勾选协议'})
        print("4444444444444")
        # 校验邮箱是否合法
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
            return render(request,'register.html',{'errmsg':'邮箱不合法'})
        print("222222222222")
        #校验用户名是否存在
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        if user:
            # 用户名已存在
            return render(request,'register.html',{'errmsg':'用户名已存在，请重新输入'})
        print("33333333333333")
        # 业务处理：用户注册
        user = User.objects.create_user(username,email,password)
        user.is_active = 0
        user.save()
        print("111111111111111111", user)

        # 返回应答:跳转到首页
        return redirect(reverse('goods:index'))



