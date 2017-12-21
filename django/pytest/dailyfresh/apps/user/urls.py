from django.conf.urls import url
from user.views import RegisterView,ActiveView,LoginView,LogoutView,UsercenterView,UserorderView,UsersiteView

urlpatterns = [
    # url(r'^register$',views.register,name='register'), #注册页面显示
    url(r'^register$',RegisterView.as_view(),name='register'),#注册
    url(r'^active/(?P<token>.*)$',ActiveView.as_view(),name = 'active'),#激活，token做为关键字参数
    url(r'^login$',LoginView.as_view(),name = 'login'),#登录
    url(r'^logout$',LogoutView.as_view(),name = 'logout'),#登出
    url(r'^usercenter$',UsercenterView.as_view(),name = 'usercenter'),#用户中心
    url(r'^userorder$',UserorderView.as_view(),name = 'userorder'),#用户订单
    url(r'^usersite$',UsersiteView.as_view(),name = 'usersite'),#用户收货地址
]
