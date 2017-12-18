from django.conf.urls import include, url
from booktest import views
# from booktest.views import MyView

urlpatterns = [
    url(r'^send$',views.send),
    # url(r'^session_set/$',views.session_set),
    # url(r'^session_get/',views.session_get),
    # url(r'^mine/$',MyView.as_view(),name = 'my-view'),
]
