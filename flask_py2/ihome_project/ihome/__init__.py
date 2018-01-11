#encoding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
from config import config_map 
import redis
import logging
from logging.handlers import RotatingFileHandler
from ihome.utils.commons import ReConverter
 

# 创建数据库工具
db = SQLAlchemy()

# 创建Redis连接实例
redis_store = None

# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)  # 调试debug级

# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)

# 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')

# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)

# 为全局的日志工具对象（flask app使用的）添加日记录器
logging.getLogger().addHandler(file_log_handler)


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

    # 注册自定义的转换器
    app.url_map.converters["re"] = ReConverter

    # 注册接口蓝图
    from ihome import api_v1_0 #方式db循环导入，什么时候用什么时候导入，放在函数内部
    #  app.register_blueprint(api_v1_0.api,url_prefix="/api/v1.0")指明版本号
    app.register_blueprint(api_v1_0.api,url_prefix="/api/v1.0")

    from ihome import web_page
    app.register_blueprint(web_page.html)

    return app