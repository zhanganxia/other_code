from django.conf.urls import url
from django.contrib.auth.decorators import login_required #login_required装饰器
from user.views import RegisterView,ActiveView,LoginView,LogoutView,UsercenterView,UserorderView,UsersiteView

urlpatterns = [
    url(r'^register$',RegisterView.as_view(),name='register'),#注册
    url(r'^active/(?P<token>.*)$',ActiveView.as_view(),name = 'active'),#激活，token做为关键字参数
    url(r'^login$',LoginView.as_view(),name = 'login'),#登录
    url(r'^logout$',LogoutView.as_view(),name = 'logout'),#登出
    url(r'^usercenter$',login_required(UsercenterView.as_view()),name = 'usercenter'),#用户中心
    url(r'^userorder$',login_required(UserorderView.as_view()),name = 'userorder'),#用户订单
    url(r'^usersite$',login_required(UsersiteView.as_view()),name = 'usersite'),#用户收货地址
]
# login_required()会自动判断用户有没有登录；@login_required装饰器不能直接装饰类视图
# 用户未登录访问usercenter页面的URL跳转路径：accounts/login/?next=/user/usercenter
# 用户没有登录，点击页面会直接跳转到：内置的登录URL："/account/login"，我们需要将此路径改为自己需要的额路径