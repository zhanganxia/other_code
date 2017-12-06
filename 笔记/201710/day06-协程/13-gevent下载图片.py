import gevent
import urllib.request #网络模块
from gevent import monkey
import os

#打补丁,让gevent识别耗时操作
monkey.patch_all()

#下载图片的任务
def download_img(img_url,img_name):
    #根据地址打开资源路径
    response = urllib.request.urlopen(img_url)
    try:
        with open(img_name,"wb") as file:
            while True:
                #读取资源理解的数据
                img_data = response.read(1024)
                if img_data:
                    #把获取的文件二进制数据写入到指定文件
                    file.write(img_data)
                else:
                    break

    except Exception as e:
        print("图片下载异常:",e)
    else:
        print("%s图片下载成功" % img_name)


if not os.path.exists("./img"):
    os.mkdir("./img")
       
with open("download.txt","r") as f:
    lines = f.readlines()
    #print(lines)
index = 1
for img_url in lines:
    img_url = img_url.strip()
    img_name = "img/" + str(index) + '.jpg'
    download_img(img_url,img_name)
    index += 1





