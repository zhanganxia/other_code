import gevent
import urllib.request#网络模块
from gevent import monkey

#打补丁,让gevent识别耗时操作
monkey.patch_all()

#下载图片的任务
def download_img(img_url,img_name):
    #根据地址打开资源路径
    response = urllib.request.urlopen(img_url)
    try:
        with open(img_name,"wb") as file:
            while True:
                #读取资源路径的数据
                img_data = response.read(1024)
                if img_data:
                    #把获取的文件二进制数据写入到指定文件
                    file.write(img_data)
                else:
                    break
    except Exception as e:
        print("图片下载异常:",e)
    else:
        print("%s图片下载成功"% img_name)
#定义资源路径
img_url = ""

#创建协程对象
gevent.joinall([
    #创建协程对象
    gevent.spawn(download_img,img_url,"1.jpg")
])
