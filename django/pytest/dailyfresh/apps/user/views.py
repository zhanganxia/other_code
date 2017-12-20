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

        # 给用户的注册邮箱发送激活邮件，激活邮件中需要包含激活链接（每一个用户的激活链接不一样，点击需要识别用户的身份）
        # 激活链接的设计：/user/active/用户ID
        # 以上激活链接的弊端：直接放置用户ID，会导致有人可能恶意请求网站
        # 解决方法：对用户ID加密，使用itsdangerous -->dumps()方法加密；loads()方法解密
        
        # 1.加密用户身份信息，生成激活token（这里使用的密钥是借助django自己的密钥）
        serializer = Serializer(settings.SECRET_KEY,3600)
        info = {'confirm':user.id}
        # info = {'confirm':999}

        token = serializer.dumps(info)#加密数据，bytes类型
        token = token.decode('utf-8') #str

        # 3.给用户发送激活邮件
        # 组织邮件内容
        subject = '天天生鲜欢迎信息'
        message = ''
        html_message = '<h1>%s,欢迎您成为天天生鲜注册会员</h1>请点击以下链接激活您的账户<br><a href="http:127.0.0.1:8000/user/active/%s">http:127.0.0.1:8000/user/active/%s</a>'%(username,token,token)
        sender = settings.DEFAULT_FROM_EMAIL 
        receiver = [email]
        print(receiver)
        send_mail(subject,message,sender,receiver,html_message=html_message)

        # 返回应答:跳转到首页
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
        return render(request,'login.html')