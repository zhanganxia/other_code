# coding:utf-8
from flask import jsonify,current_app
from . import api
from ihome.utils.captcha.captcha import captcha
from ihome import redis_store,constance
from ihome.utils.response_code import RET
# GET /image_codes/图片验证码编号
# ?:代表过滤资源  /:代表获取某一个特定的资源
@api.route('/image_codes/<image_code_id>')
def get_image_code(image_code_id):
    """提供图片验证码"""

    # 提取参数  image_code_id（不用提取用和校验）
    # 生成验证码图片
    # 名字，真实验证码 验证码图片数据
    name,text,image_data = captcha.generate_captcha()

    # 保存验证码的真实值，和这个验证码的编号,redis中，有效期
    # redis数据类型：字符串，列表，hash，set...
    # key：val 采用字符串
    # "image_code_编号1":"真实值"
    
    # redis_store.set(key,value)
    # redis_store.set("image_code_%s"%image_code_id,text)
    # redis_store.expire("image_code_%s"%image_code_id,constance.IMAGE_CODE_REDIS_EXPIRES)
    try:
        redis_store.setex("image_code_%s" % image_code_id,constance.IMAGE_CODE_REDIS_EXPIRES,text)
    except Exception as e:
        # 日志中记录异常信息
        current_app.logger.error(e)
        return jsonify(errcode=RET.DBERR,errmsg="数据库异常")
    # 返回验证码图片
    return image_data,200,{"Content-Type":"image/jpg"}