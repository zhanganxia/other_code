from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View
from user.models import User,Address
from goods.models import GoodsSKU
from order.models import OrderInfo,OrderGoods
import re
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer #实现数据的加密/解密/过期时间
from itsdangerous import SignatureExpired
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.core.mail import send_mass_mail
from celery_tasks.sendmail_task import send_register_active_email
from django.contrib.auth import authenticate,login,logout #django自己的认证系统
from django_redis import get_redis_connection
from utils.mixin import LoginRequiredView,LoginRequiredMixin

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

# /user/usercenter
# class UsercenterView(View):
# class UsercenterView(LoginRequiredView):
class UsercenterView(LoginRequiredMixin,View):
    '''用户中心页面显示'''
    def get(self,request):
        # 返回用户中心页面的显示
        # print(UsercenterView.__mro__) #查看调用类的执行顺序
        # 获取用户默认的信息
        user = request.user
        address = Address.objects.get_default_address(user)
        # 获取用户的浏览记录
        # 连接到redis数据库
        # 方式一
        # from redis import StrictRedis
        # conn = StrictRedis(host='127.0.0.1',port=6379,db=6)
        # 方式二
        conn = get_redis_connection('default')
        history_key = 'history_%d'%user.id
        # 获取用户最新浏览的5个商品的id
        sku_ids = conn.lrange(history_key,0,4)

        # select * from df_goods_sku where id in (3,2,1)
        # 注意：我们需要保证查询的顺序和取出的顺序是一致的，数据库中查出来的数据顺序是：按id从小向大排序
        # 保证用户浏览的顺序的两种方法：

        #方法一：只查询一次
        # skus = GoodsSKU.objects.filter(id__in=sku_ids)
        # skus_li = []
        # for sku_id in sku_ids:
        #     for sku in skus:
        #         if sku.id == int(sku_id):
        #             skus_li.append(sku)

        # 方法二：查询5次
        skus = []
        for sku_id in sku_ids:
            # 根据sku_id获取商品的信息
            sku = GoodsSKU.objects.get(id=sku_id)
            # 添加到skus列表中
            skus.append(sku)

        # 组织模板上下文
        context = {
            'skus':skus,
            'page':'usercenter',
            'address':address
        }

        return render(request,'user_center_info.html',context)

# /user/userorder/页码
# class UserorderView(View):
# class UserorderView(LoginRequiredView):
class UserorderView(LoginRequiredMixin,View):
    '''用户订单页面显示'''
    def get(self,request,page):
        # 获取登录的用户
        user = request.user
        # 获取用户的订单信息
        orders = OrderInfo.objects.filter(user=user).order_by('-create_time')
        # 遍历获取每个订单中订单商品的信息
        for order in orders:
            # 获取和order订单关联的订单商品的信息
            order_skus = OrderGoods.objects.filter(order=order)
            # 遍历计算订单中每一个商品的小计
            for order_sku in order_skus:
                # 计算小计
                amount = order_sku.count*order_sku.price
                # 给order_sku增加属性amount，保存订单商品的小计
                order_sku.amount = amount

            # 获取订单支付状态的名称
            order.status_name = OrderInfo.ORDER_STATUS[order.order_status]
            
            # 计算订单的实付款
            order.total_pay = order.total_price + order.transit_price
            
            # 给order增加属性order_skus,保存订单商品的信息
            order.order_skus =  order_skus

        # 分页
        paginator = Paginator(orders,2)
        # 处理页码
        page = int(page)
        if page > paginator.num_pages or page <= 0:
            # 默认显示第1页
            page = 1
        # 获取第page页的page对象
        order_page = paginator.page(page)
        # 页码处理(页面最多只显示5个页码)
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1,num_pages + 1)
        elif page <= 3:
            pages =  range(1,6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4,num_pages + 1)
        else:
            pages = range(page - 2,page + 3)

        # 组织模板上下文
        context = {
            'order_page':order_page,
            'pages':pages,
            'page':'order'
        }
        return render(request,'user_center_order.tmpl',context)

# /user/usersite
# class UsersiteView(View):
# class UsersiteView(LoginRequiredView):
class UsersiteView(LoginRequiredMixin,View):
    '''用户收货地址页面显示'''
    def get(self,request):
        # 获取登录用户
        user = request.user
        # 获取默认地址
        address = Address.objects.get_default_address(user)
        return render(request,'user_center_site.html',{'page':'usersite','address':address})
    
    def post(self,request):
        '''添加地址'''
        # 接收参数
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')
        # 参数校验
        if not all([receiver,addr,phone]):
            return render(request,'user_center_site.html',{'errmsg':'数据不完整'})
        # 业务处理：添加收货地址
        # 如果用户的地址已经存在默认收货地址，新添加的地址做为非默认地址，否则添加的地址做为默认地址
        # 获取当前用户的默认地址
        user = request.user
        address = Address.objects.get_default_address(user)
        is_default = True
        if address:
            # 已经有默认地址了：
            is_default = False

        # 添加地址
        Address.objects.create(user=user,receiver=receiver,addr=addr,zip_code=zip_code,phone=phone,is_default=is_default)
        # 返回应答：跳转到收货地址页面
        return redirect(reverse('user:usersite'))#get

