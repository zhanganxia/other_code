from django.conf.urls import url
from django.contrib.auth.decorators import login_required #login_required装饰器
from user.views import RegisterView,ActiveView,LoginView,LogoutView,UsercenterView,UserorderView,UsersiteView

urlpatterns = [
    url(r'^register$',RegisterView.as_view(),name='register'),#注册
    url(r'^active/(?P<token>.*)$',ActiveView.as_view(),name = 'active'),#激活，token做为关键字参数
    url(r'^login$',LoginView.as_view(),name = 'login'),#登录
    url(r'^logout$',LogoutView.as_view(),name = 'logout'),#登出
    # url(r'^usercenter$',login_required(UsercenterView.as_view()),name = 'usercenter'),#用户中心
    # url(r'^userorder$',login_required(UserorderView.as_view()),name = 'userorder'),#用户订单
    # url(r'^usersite$',login_required(UsersiteView.as_view()),name = 'usersite'),#用户收货地址

    url(r'^usercenter$',UsercenterView.as_view(),name = 'usercenter'),#用户中心
    url(r'^userorder/(?P<page>\d+)$',UserorderView.as_view(),name = 'userorder'),#用户订单
    url(r'^usersite$',UsersiteView.as_view(),name = 'usersite'),#用户收货地址
]

# 重写View的as_view方法，在重写的方法中返回login_required,在路由中使用的还是之前的方法：类名.as_view()的形式