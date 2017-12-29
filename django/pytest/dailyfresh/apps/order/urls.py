from django.conf.urls import url
from order.views import OrderView
urlpatterns = [
    url(r'^order$',OrderView.as_view(),name='order'),#提交订单页面显示
]
