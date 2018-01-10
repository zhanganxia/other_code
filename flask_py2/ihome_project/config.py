#encoding=utf-8
import redis

# 配置信息(两种方式定义：类、单一文件)
class Config(object):
    '''配置信息'''
    SECRET_KEY = "ADSGJKKGFFAADadsf"
    
    # flask-session的配置信息
    SESSION_TYPE = "redis" #指明session数据保存在redis中
    SESSION_USE_SIGNER = True #指明对cookie中保存的session_id进行加密防护
    PERMANENT_SESSION_LIFETIME = 3*24*60*60 #session有效期，单位秒


class DevelopmentConfig(Config):
    '''开发环境的配置信息'''
    DEBUG = True
    
    # 数据库的配置信息
    
    SQLALCHEMY_DATABASE_URI = "mysql://：test:mysql@127.0.0.1:3306/ihome"
    SQLALCHEMY_TRACK_MODIFICATIONS = True #Flask-SQLAlchemy 将会追踪对象的修改并且发送信号

    # redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    REDIS_DB = 0

    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT,db=1)#使用redis数据库 
    

class ProductConfig(Config):
    """生产环境（线上环境）配置信息"""
    pass

config_map = {
    "product":ProductConfig,
    "develop":DevelopmentConfig
}