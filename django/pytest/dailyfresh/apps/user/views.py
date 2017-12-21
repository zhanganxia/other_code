from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View
from user.models import User
import re
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer #实现数据的加密/解密/过期时间
from itsdangerous import SignatureExpired
from django.core.mail import send_mail
from django.core.mail import send_mass_mail
from celery_tasks.sendmail_task import send_register_active_email
from django.contrib.auth import authenticate,login,logout #django自己的认证系统



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
        # 校验邮箱是否合法
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
            return render(request,'register.html',{'errmsg':'邮箱不合法'})
        #校验用户名是否存在
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        if user:
            # 用户名已存在
            return render(request,'register.html',{'errmsg':'用户名已存在，请重新输入'})
        # 业务处理：用户注册
        user = User.objects.create_user(username,email,password)
        user.is_active = 0
        user.save()
        
        # 1.加密用户身份信息，生成激活token（这里使用的密钥是借助django自己的密钥）
        serializer = Serializer(settings.SECRET_KEY,3600)
        info = {'confirm':user.id}
        # info = {'confirm':999}

        token = serializer.dumps(info)#加密数据，bytes类型
        token = token.decode('utf-8') #str

        # 3.借助selery给用户发送激活邮件
        send_register_active_email.delay(email,username,token)
        return redirect(reverse('goods:index'))

# 2./user/active/激活token信息
class ActiveView(View):
    '''激活'''
    def get(self, request, token):
        '''激活处理'''
        serializer = Serializer(settings.SECRET_KEY,3600)
        try:
            # 解密数据
            info = serializer.loads(token)
            # 获取待激活的用户的id
            user_id = info['confirm']
            # 业务处理：激活帐号
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # 返回应答：跳转到登录页面
            return redirect(reverse('user:login'))
        except SignatureExpired:
            # 激活链接已失效
            return HttpResponse('激活链接已失效')

# /user/login
class LoginView(View):
    """登录"""
    def get(self, request):
        # 显示
        # 2.判读cookie中是否存入username
        if 'username' in request.COOKIES:
            # 记住了用户名
            username = request.COOKIES['username']
            checked = 'checked'
        else:            
            #没有用户名 
            username = ''
            checked = ''
        return render(request,'login.html',{'username':username,'checked':checked})

    def post(self,request):
        ''''登录处理'''
        # 1.接收参数
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        remember = request.POST.get('remember')
        # 2.参数校验
        if not all([username,password]):
            return render(request,'login.html',{'errmsg':'输入的数据不完整'})
        # 3.业务处理：登录校验
        # django认证系统中的：authenticate(),认证一组给定的用户名和密码
        user = authenticate(username=username, password=password)
        if user is not None:
            #用户名密码正确
            if user.is_active:
                # django认证系统中记录登录状态：login(),它接受一个HttpRequest对象和一个User对象，记录登录用户的ID存在session中                
                login(request,user) 

                # 获取登录后要跳转到的next地址，默认跳转到首页
                next_url = request.GET.get('next',reverse('goods:index'))

                # 跳转到next_url
                response = redirect(next_url)
                #1.用户名密码正确后判断是否勾选‘记住密码’
                if remember == 'on':
                    response.set_cookie('username',username,max_age = 7*24*3600)
                else:
                    # 不记住用户名，密码
                    response.delete_cookie('username')
                return response
            else:
                return render(request,'login.html',{'errmsg':'用户是无效的'})
        else:
            # 用户名或密码不正确
            return render(request,'login.html',{'errmsg':'用户名或密码错误'})
        # 4.返回应答

# /user/logout
class LogoutView(View):
    '''退出登录'''
    def get(self,request):
        # 清除用户的登录状态:logout()
        logout(request)
        # 返回应答：跳转到首页
        return redirect(reverse('goods:index'))

from utils.mixin import LoginRequiredView

# /user/usercenter
# class UsercenterView(View):
class UsercenterView(LoginRequiredView):
    '''用户中心页面显示'''
    def get(self,request):
        # 返回用户中心页面的显示
        return render(request,'user_center_info.html',{'page':'usercenter'})

# /user/userorder
# class UserorderView(View):
class UserorderView(LoginRequiredView):
    '''用户定点页面显示'''
    def get(self,request):
        return render(request,'user_center_order.html',{'page':'userorder'})

# /user/usersite
# class UsersiteView(View):
class UsersiteView(LoginRequiredView):
    '''用户收货地址页面显示'''
    def get(self,request):
        return render(request,'user_center_site.html',{'page':'usersite'})

