from django.conf.urls import include, url
from booktest import views

urlpatterns = [
    url(r'^jingtai$',views.jingtai),
    url(r'^pic_upload$',views.pic_upload),
    url(r'^pic_handle$',views.pic_handle),
    url(r'^pic_show$',views.pic_show),
    url(r'^page(\d*)/$',views.pagelist),
    url(r'^area$',views.area_select),
    url(r'^areas$',views.areas),
]




