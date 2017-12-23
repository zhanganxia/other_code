from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from django.conf import settings
import os

# 保存文件的时候，django系统会调用Storage类中的save方法，save方法内部会调用文件存储类中的__save方法
# _save方法的返回值会存储在数据库的一个字段中
# 自定义文件存储类
class FDFSStorage(Storage):
    '''fastdfs系统文件存储类'''
    def _open(self,name,mode='rb'):
        '''打开文件'''
        pass

    def _save(self,name,content):
        '''保存文件时使用'''
        # name:文件的名字
        # content:包含上传文件内容的file对象

        # 把文件上传到fastdfs系统中
        client = Fdfs_client(os.path.join(settings.BASE_DIR,'utils/fdfs/client.conf'))
        
        # 获取上传文件内容
        content = content.read()
        ret = client.upload_by_buffer(content)

        # 判断上传文件是否成功
        if ret.get('Status') !='Upload successed.':
            print('上传失败')
            raise Exception('上传文件到fdfs系统失败')

        # 获取文件的ID
        file_id = ret.get('Remote file_id')

        # 返回文件ID
        return file_id
# 在调用save方法之前，django系统会先调用exists方法，判断文件的系统是否存在
    def exists(self,name):
        return False

    def url(self,name):
        '''返回一个可以访问到文件的url路径'''
        # name:文件id
        return 'http://192.168.20.50:8888/'+name