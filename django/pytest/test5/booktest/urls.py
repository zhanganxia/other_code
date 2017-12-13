from django.conf.urls import include, url
from booktest import views

urlpatterns = [
    url(r'^jingtai$',views.jingtai)
]