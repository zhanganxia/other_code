from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from blog.models import Article,Category
from blog.forms import BlogCommentForm
import markdown2

class IndexView(ListView):
    '''博客首页'''
    # 制定获取的model数据列表的名字
    # context_object_name = 'article_list'

    def get(self,request):
        '''获取已发布的文章列表，并转为html格式'''
        article_list = Article.objects.filter(status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body,)
        return render(request,'index.html',{'article_list':article_list})
    
    # 为上下文添加额外的变量，以便在模板中访问
    def get_context_data(self,**kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        return super(IndexView, self).get_context_data(**kwargs)

class ArticleDetailView(DetailView):
    '''显示文章详情'''
    model = Article
    template_name = 'detail.html'
    context_object_name = "article"

    # pk_url_kwarg用于接受来自url中的参数作为主键
    pk_url_kwarg = 'article_id'

    # 从数据库中获取id为pk_url_kwargs的对象
    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        obj.body = markdown2.markdown(obj.body)
        return obj

class CategoryView(ListView):
    '''文章分类'''
    def get(request,self):
        category = request.cate_id
        article_list = Article.objects.filter(category=category,status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body,)
        return render(request,'index.html',{'article_list':article_list})   
    
    # 为上下文添加额外的变量，以便在模板中访问
    def get_context_data(self,**kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        return super(IndexView, self).get_context_data(**kwargs)