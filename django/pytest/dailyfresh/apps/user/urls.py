from django.conf.urls import url
from user.views import RegisterView

urlpatterns = [
    # url(r'^register$',views.register,name='register'), #注册页面显示
    url(r'^register$',RegisterView.as_view(),name='register'),#注册
]
