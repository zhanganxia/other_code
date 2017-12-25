from celery import Celery #导入celery的包
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader

# 初始化django所依赖的环境，在启动worker的一端打开
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
django.setup()
# 导入类的代码必须在引入django环境代码的后面，否则还是会出错
from goods.models import GoodsType,IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner

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

@app.task
def generate_static_index_html():
    '''生成一个静态首页文件'''
    # 获取商品分类信息
    types = GoodsType.objects.all()
    
    # 获取首页轮播商品的信息
    goods_banner = IndexGoodsBanner.objects.all().order_by('index')

    # 获取首页促销活动的信息
    promotion_banner = IndexPromotionBanner.objects.all().order_by('index')

    # 获取首页分类商品展示信息
    # types_goods_banner = IndexTypeGoodsBanner.objects.all().order_by('index')
    for type in types:
        title_banner = IndexTypeGoodsBanner.objects.filter(type=type,display_type=0).order_by('index')
        image_banner = IndexTypeGoodsBanner.objects.filter(type=type,display_type=1).order_by('index')
        type.title_banner = title_banner
        type.image_banner = image_banner

    # 获取用户购物车商品的数目
    cart_count = 0

    # 组织上下文
    context = {
        'types':types,
        'goods_banner':goods_banner,
        'promotion_banner':promotion_banner,
        'cart_count':cart_count
    }
    # 渲染产生静态首页html内容
    # 1.加载模板，获取模板对象
    temp = loader.get_template('static_index.html')

    # 2.模板渲染，获取模板对象
    static_html = temp.render(context)

    # 创建一个静态首页文件
    save_path = os.path.join(settings.BASE_DIR,'static/index.html')
    with open(save_path,'w') as f:
        f.write(static_html)
