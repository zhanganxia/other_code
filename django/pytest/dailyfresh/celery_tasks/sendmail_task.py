from celery import Celery #导入celery的包
from django.conf import settings
from django.core.mail import send_mail

# 初始化django所依赖的环境，在启动worker的一端打开
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")

# 创建一个celery对象
# redis做为中间人(broker)，使用redis的5号数据库
app = Celery('celery_tasks.sendmail_task',broker='redis://127.0.0.1:6379/5')

# 定义任务函数
@app.task
def send_register_active_email(to_email,username,token):
    '''注册时发送激活邮件'''
    # 组织邮件内容
    subject = '天天生鲜欢迎信息'
    message = ''
    sender = settings.DEFAULT_FROM_EMAIL
    receiver = [to_email]
    html_message = '<h1>%s,欢迎您成为天天生鲜注册会员</h1>请点击以下链接激活您的账户<br><a href="http:127.0.0.1:8000/user/active/%s">http:127.0.0.1:8000/user/active/%s</a>'%(username,token,token)

    import time
    time.sleep(5)
    send_mail(subject,message,sender,receiver,html_message=html_message)

# 注意：celery发出任务时不是发出任务的代码，发出的是任务函数的名字和所需的参数

