from django.db import models
from db.base_model import BaseModel

class Article(BaseModel):
    '''定义文章模型类'''
    # 文章的状态
    STATUS_CHOICES = (
        ('d','part'),
        ('p','Published'),
    )
    title = models.CharField(max_length=70,verbose_name="'标题'")
    body = models.TextField(verbose_name='正文')

    status = models.CharField(max_length=1,choices=STATUS_CHOICES,verbose_name="文章状态")
    abstract = models.CharField(max_length=54,blank=True,null=True,verbose_name="摘要",help_text="可选项，若为空格则摘取正文前54个字符")

    # 阅读量
    views = models.PositiveIntegerField(default=0,verbose_name="浏览器")
    # 点赞数
    likes = models.PositiveIntegerField(default=0,verbose_name="点赞数")
    # 是否置顶
    topped = models.BooleanField(default=False,verbose_name="置顶")
    # 目录分类
    category = models.ForeignKey('Category',verbose_name="分类",null=True,on_delete=models.SET_NULL)

    class Meta:
        db_table = 'blog_article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class Category(BaseModel):
    '''文章分类模型类'''
    name = models.CharField(max_length=20,verbose_name="类名")

    class Meta:
        db_table = 'blog_category'
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
