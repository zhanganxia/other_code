from django.conf.urls import url
from user import views

urlpatterns = [
    url(r'^register$',views.register,name='register'), #注册页面显示
    # url(r'^register_handle$',views.register_handle,name='register_handle'),#注册页面处理
]
