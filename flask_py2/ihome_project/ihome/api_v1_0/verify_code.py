# coding:utf-8
from flask import jsonify,current_app,request
from . import api
from ihome.utils.captcha.captcha import captcha
from ihome import redis_store,constants,db
from ihome.utils.response_code import RET
from ihome.models import User
import random
from ihome.libs.yuntongxun.sms import CCP


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
    # redis_store.expire("image_code_%s"%image_code_id,constants.IMAGE_CODE_REDIS_EXPIRES)
    try:
        redis_store.setex("image_code_%s" % image_code_id,constants.IMAGE_CODE_REDIS_EXPIRES,text)
    except Exception as e:
        # 日志中记录异常信息
        current_app.logger.error(e)
        return jsonify(errcode=RET.DBERR,errmsg="数据库异常")
    # 返回验证码图片
    return image_data,200,{"Content-Type":"image/jpg"}


#GET /sms_codes/手机号？image_code_id=xxx&image_code_text=xxx
@api.route('/sms_codes/<re(r"1[3456789]\d{9}"):mobile>')
def send_sms_code(mobile):
    """发送短信验证码"""
    # 提取参数
    image_code_id = request.args.get("image_code_id")
    image_code_text = request.args.get("image_code_text")

    # 校验参数    
    if not all([image_code_id,image_code_text]):
        return jsonify(errcode=RET.PARAMERR,errmsg="参数不完整")

    #验证图片验证的正确性：
    # 根据编号取出图片验证码的真实值：redis
    try:
        real_image_code_text = redis_store.get("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errcode=RET.DBERR,errmsg="数据库异常")
    
    # 判断图片验证码的值是否过期
    if real_image_code_text is None:
        # 表示不存在或过期
        return jsonify(errcode=RET.NODATA,errmsg="图片验证码已过期")

    # 在redis中删除图片验证码的真实值，防止用户对同一个验证码进行二次尝试
    try:
        redis_store.delete("image_code_%s"%image_code_id)
    except Exception as e:
        current_app.logger.error(e)

    # 将用户填写的与真实值进行对比
    if real_image_code_text.lower() != image_code_text.lower():
        # 表示用户填写图片验证码错误
        return jsonify(errcode=RET.DATAERR,errmsg="图片验证码错误")
    
    # 如果相同
    # 查询数据库，判断手机号是否注册过
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
    else:
        if user is not None:
            # 表示手机号注册过
            return jsonify(errcode=RET.DATAEXIST, errmsg="手机号已注册过")
    
    # 手机号没有注册过
    # 判断是否在60秒内发送过短信，如果发送过，则提前终止
    try:
        redis_store.get("send_sms_code_flag_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if flag is not None:
            # 表示60秒内有发送记录
            return jsonify(errcode=RET.REQERR,errmsg="发送过于频繁")

    # 生成短信验证码
    # %06d表示格式化显示，至少6位数字，不足6为前面补0
    sms_code = "%06d" % random.randint(0, 999999)

    # 保存手机号和短信验证码
    try:
        redis_store.setex("sms_code_%s"%mobile,constants.SMS_CODE_REDIS_EXPIRES,sms_code)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errcode=RET.DBERR,errmsg="保存短信验证码异常")
    
    # 保存发送的记录到redis中
        try:
            redis_store.setex("send_sms_code_flag_%s"% mobile,constants.SEND_SMS_CODE_INTERVAL,1)
        except Exception as e:
            current_app.logger.error(e)
    
    # 发送短信验证码
    try:
        ccp = CCP()
        result = ccp.send_template_sms(mobile,[sms_code,str(constants.IMAGE_CODE_REDIS_EXPIRES // 60)],
                                constants.SMS_CODE_TEMPLATE)
    
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errcode=RET.THIRDERR,errmsg="发送短信异常")
    
    if result == -1:
        return jsonify(errcode=RET.THIRDERR,errmsg="发送短信失败")
    else:
        return jsonify(errcode=RET.OK,errmsg="发送短信成功")

# 1.保存上一次发送短信的时间
# 2.根据上一次保存的时间与再发送的事件进行计算，求取差值，如果小于60秒，就不再发送
