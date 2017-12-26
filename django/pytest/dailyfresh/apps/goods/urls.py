from django.conf.urls import url
from goods.views import IndexView,DetailView

urlpatterns = [
    url(r'^index$', IndexView.as_view(), name = 'index'),#首页
    url(r'^goods/(?P<sku_id>\d+)$',DetailView.as_view(),name='detail'), #商品详情页
]
