from django.conf.urls import include, url
from booktest import views

urlpatterns = [
    url(r'^session_set/$',views.session_set),
    url(r'^session_get/',views.session_get),
]
