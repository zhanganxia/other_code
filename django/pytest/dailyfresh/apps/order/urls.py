from django.conf.urls import url
from order.views import OrderView,OrderCommitView
urlpatterns = [
    url(r'^order$',OrderView.as_view(),name='order'),#提交订单页面显示
    url(r'^commit$',OrderCommitView.as_view(),name='commit'),# 订单创建
]
