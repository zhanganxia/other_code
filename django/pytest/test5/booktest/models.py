from django.db import models
# Create your models here.
class AreaInfo(models.Model):
    atitle=models.CharField('标题',max_length=30) #名称
    aParent=models.ForeignKey('self',null=True,blank=True) #关系

    # 在模型类中定义str方法，用于对象转换字符串
    def __str__(self):
        return self.atitle

    def title(self):
        return self.atitle

    # 在模型类中封装方法，访问关联对象的成员
    def parent(self):
        return self.aParent.atitle

    title.admin_order_field = 'atitle'

    # 修改列标题：short_description='区域名称'
    title.short_description = '区域名称'

    parent.short_description = '父级区域名称'


class PicTest(models.Model):
    pic = models.ImageField(upload_to='booktest/')




    