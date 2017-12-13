from django.conf.urls import url
from booktest import views

urlpatterns = [
    url(r'^index$',views.index),
    url(r'^booklist$',views.booklist),
    url(r'^area$',views.area),
    # url(r'^(\d+)/(\d+)/$',views.index1),
    url(r'^(?P<parameter1>\d+)/(?P<parameter2>\d+)/$',views.index2),
    url(r'^method1/$',views.method1),
    url(r'^method2/$',views.method2),
    url(r'^method3/$',views.method3),
    url(r'^get$',views.get),
    url(r'^getwish$',views.getwish),
    # post 请求的POST属性：准备表单
    url(r'^post/$',views.post),
    # 获取表单提交的参数
    url(r'^post1/$',views.post1),
    url(r'^json1/$',views.json1),
    url(r'^json2/$',views.json2)
]