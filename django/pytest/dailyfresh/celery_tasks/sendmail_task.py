from celery import Celery #导入celery的包
from django.conf import settings
from django.core.mail import send_mail

# 初始化django所依赖的环境，在启动worker的一端打开
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")

# 创建一个celery对象
# redis做为中间人，使用redis的5号数据库
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

# 1.在另一终端启动celery任务，启动命令：celery -A celery_tasks.sendmail_task worker -l info

    # - ** ---------- [config]
    # - ** ---------- .> app:         celery_tasks.sendmail_task:0x7fc257dcc940
    # - ** ---------- .> transport:   redis://127.0.0.1:6379/5
    # - ** ---------- .> results:     disabled://
    # - *** --- * --- .> concurrency: 4 (prefork)
    # -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
    # --- ***** ----- 
    # -------------- [queues]
    #                 .> celery           exchange=celery(direct) key=celery                
    # [tasks]
    # . celery_tasks.sendmail_task.send_register_active_email

# 2.在注册页面中填写并提交注册信息：
# [2017-12-20 18:08:47,558: INFO/MainProcess] Received task: celery_tasks.sendmail_task.send_register_active_email[cfae6acf-27e0-497e-aba4-5f0d617cde13]  

# 3.提交页面后终端的报错信息，原因：在执行此任务的时候，并没有启动项目，在执行此任务的时候我们用到了django项目的配置项：sender = settings.DEFAULT_FROM_EMAIL，所以需要对此任务进行：依赖环境的初始化
# ERROR/ForkPoolWorker-4] Task celery_tasks.sendmail_task.send_register_active_email[cfae6acf-27e0-497e-aba4-5f0d617cde13] raised unexpected: ImproperlyConfigured('Requested setting DEFAULT_FROM_EMAIL, but settings are not configured. You must either define the environment variable DJANGO_SETTINGS_MODULE or call settings.configure() before accessing settings.',)

