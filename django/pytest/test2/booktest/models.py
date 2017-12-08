from django.db import models


class BookInfo(models.Model):
    '''定义图书模型类BookInfo'''
    btitle = models.CharField(max_length=20)
    bpub_date = models.DateField() #发布日期
    bread = models.IntegerField(default=0) #阅读量
    bcommet = models.IntegerField(default=0) #评论量
    isDelete = models.BooleanField(default=False) #逻辑删除
    class Meta: #元信息类
        db_table = 'bookinfo' #指定表的名称


class HeroInfo(models.Model):
    '''定义英雄模型类HeroInfo'''
    hname = models.CharField(max_length=20) #英雄姓名
    hgender = models.BooleanField(default=True) #英雄性别
    isDelete = models.BooleanField(default = False) #逻辑删除
    hcontent = models.CharField(max_length=100) #英雄描述信息
    hbook = models.ForeignKey('BookInfo') #英雄与图书表的关系为一对多，所以属性定义在英雄模型中
