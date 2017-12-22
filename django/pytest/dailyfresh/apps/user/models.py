from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel

#使用django默认的认证系统
# python manage.py crestesuperuser-->auth_user-->User模型类
class User(AbstractUser,BaseModel):
    '''用户模型类'''

    class Meta:
        db_table = 'df_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class AddressManager(models.Manager):
    '''模型管理器类'''
    # 添加模型管理器类的场景：
        # 1.改变原有查询的结果集
        # 2.添加额外的方法：操作self所在的模型类对应的数据表(增删改查)
    def get_default_address(self,user):
        '''获取user用户的默认地址'''
        # self.model-->获取self对象所在的模型类，类名发生变化的时候此处的代码不会变
        # Address.objects.get_default_address(user)        
        try:
            # get是Manager的方法
            address = self.get(user=user,is_default=True)
        except self.modelS.DoesNotExist:
            address = None

        return address

class Address(BaseModel):
    '''地址模型类'''
    user = models.ForeignKey('User',verbose_name='所属账户')
    receiver = models.CharField(max_length=20,verbose_name='收件人')
    addr = models.CharField(max_length=256,verbose_name='收件地址')
    zip_code = models.CharField(max_length=6,null=True,verbose_name='邮政编码')
    phone = models.CharField(max_length=11,verbose_name='联系电话')
    is_default = models.BooleanField(default=False,verbose_name='是否默认删除')

    # 自定义模型管理器类的对象
    objects = AddressManager()
    class Meta:
        db_table = 'df_address'
        verbose_name = '地址'
        verbose_name_plural = verbose_name