from django.db import models


class BookInfoManager(models.Manager):
    '''自定义图书管理器类改变查询结果集'''
    def total(self):
        return super().all().filter(isDelete = False)
    
    def shuminghao(self,obj):
        '''给所有的书名加上书名号'''
        for i in obj:
            i.btitle = "《%s》"%i.btitle
        return obj

class BookInfo(models.Model):
    '''定义图书模型类BookInfo'''
    #使用和objects相同的名称来实例化，objects比原来的功能多了一个total方法
    objects = BookInfoManager()

    btitle = models.CharField(max_length=20)
    bpub_date = models.DateField() #发布日期
    bread = models.IntegerField(default=0) #阅读量
    bcommet = models.IntegerField(default=0) #评论量
    isDelete = models.BooleanField(default=False) #逻辑删除
    bcontext = models.CharField(max_length=100,null=True) #备注

    class Meta: #元信息类
        db_table = 'bookinfo' #指定表的名称


class HeroInfo(models.Model):
    '''定义英雄模型类HeroInfo'''
    hname = models.CharField(max_length=20) #英雄姓名
    hgender = models.BooleanField(default=True) #英雄性别
    isDelete = models.BooleanField(default = False) #逻辑删除
    hcontent = models.CharField(max_length=100) #英雄描述信息
    hbook = models.ForeignKey('BookInfo') #英雄与图书表的关系为一对多，所以属性定义在英雄模型中

class AreaInfo(models.Model):
    atitle=models.CharField(max_length=30) #名称
    aParent=models.ForeignKey('self',null=True,blank=True) #关系
