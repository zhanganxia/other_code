from django.conf.urls import url
from blog.views import IndexView,ArticleDetailView,CategoryView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^article/(?P<article_id>\d+)$', ArticleDetailView.as_view(), name='detail'),
    url(r"^category/(?P<cate_id>\d+)$", CategoryView.as_view(), name='category')
]
