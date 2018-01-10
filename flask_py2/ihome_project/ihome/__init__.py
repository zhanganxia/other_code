#encoding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
from config import config_map 
import redis
from ihome import api_v1_0 

# 创建数据库工具
db = SQLAlchemy()

# 创建Redis连接实例
redis_store = None

# 工厂模式
def create_app(run_name):
    """"工厂函数，用来创建flask应用对象
    :param run_name:flask运行的模式名字，product-生产模式 develop-开发模式
    """

    app = Flask(__name__)
    app.config.from_object(config_map[run_name])
    # 初始化数据库对象
    db.init_app(app)

    global redis_store
    redis_store = redis.StrictRedis(host=config_map[run_name].REDIS_HOST,
                                    port=config_map[run_name].REDIS_PORT,
                                    db=config_map[run_name].REDIS_DB)

    # session,引入扩展:flask-session
    # 对flak_session初始化
    Session(app)

    # 补充csrf防护
    # flask_wtf 表单扩展(未实现前后端分离)，csrf防护是这个扩展的组成部分，可以直接使用csrf防护而不使用表单
    # 对于包含了请求体的请求(POST,PUT,DELETE)
    # 防护机制：从请求的cookie中读取一个csrftoken的值，从请求体中读取一个csrf_token的值，进行比较，如果相同则允许访问，否则返回403的错误，通过钩子的方式添加上来的
    CSRFProtect(app)

    # 注册接口蓝图
    app.register_blueprint(api_v1_0.api)

    return app