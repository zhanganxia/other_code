#encoding=utf-8

from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_session import Session
from flask_wtf import CSRFProtect
import redis

app = Flask(__name__)

# 配置信息(两种方式定义：类、单一文件)
class Config(object):
    '''配置信息'''
    DEBUG = True
    
    # 数据库的配置信息
    SQLALCHEMY_DATABASE_URL = "mysql://test:mysql@127.0.0.1:3306/ihome"
    SQLALCHEMY_TRACK_MODIFICATIONS = True #Flask-SQLAlchemy 将会追踪对象的修改并且发送信号

    # redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    REDIS_DB = 0

    # flask-session的配置信息
    SESSION_TYPE = "redis" #指明session数据保存在redis中
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT,db=1)#使用redis数据库 
    SESSION_USE_SIGNER = True #指明对cookie中保存的session_id进行加密防护
    PERMANENT_SESSION_LIFETIME = 3*24*60*60 #session有效期，单位秒

app.config.from_object(Config)

# 创建数据库工具
db = SQLAlchemy(app)

# 创建Redis连接实例
redis_store = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT,db=Config.REDIS_DB)

# 启动命令扩展
manager = Manager(app)

# 初始化迁移工具
Migrate(app,db)

# 添加数据库迁移命令
manager.add_command("db",MigrateCommand)

# session,引入扩展:flask-session
# 对flak_session初始化
Session(app)

# 补充csrf防护
# flask_wtf 表单扩展(未实现前后端分离)，csrf防护是这个扩展的组成部分，可以直接使用csrf防护而不使用表单
# 对于包含了请求体的请求(POST,PUT,DELETE)
# 防护机制：从请求的cookie中读取一个csrftoken的值，从请求体中读取一个csrf_token的值，进行比较，如果相同则允许访问，否则返回403的错误，通过钩子的方式添加上来的
CSRFProtect(app)

@app.route("/")
def index():
    return "index page"

if __name__ == '__main__':
    manager.run()
    
