#coding:utf-8
from flask import request,jsonify,current_app,session

from . import api
from ihome.utils.response_code import RET
from ihome import redis_store,db
from ihome.models import User
from sqlalchemy.exc import IntegrityError #集成的错误，对应到数据中出现重复记录的错误异常
from werkzeug.security import generate_password_hash


import re

# POST /user
@api.route("/users",methods=["POST"])
def register():
    """注册"""
    # 获取参数 手机号,短信验证码,密码,确认密码 请求体（json格式）
    # get_json()方法可以直接将前端传递过来的json数据转换成字典格式的数据
    req_dict = request.get_json("")
    mobile = req_dict.get("mobile")
    sms_code = req_dict.get("sms_code")
    password = req_dict.get("password")
    password2 = req_dict.get("password2")
    # 校验参数
    if not all([mobile,sms_code,password,password2]):
        return jsonify(errcode=RET.PARAMERR,errmsg="参数不完整")
    # 验证手机号的格式
    if not re.match(r"1[3456789]\d{9}",mobile):
        # 表示手机号格式不匹配
        return jsonify(errcode=RET.DATAERR,errmsg="手机号格式错误")
    # 两次输入密码的比较
    if password2 != password:
        return jsonify(errcode=RET.DATAERR,errmsg="两次输入密码不一致")
        
    # 业务处理
        # 从redis中获取短信验证码的真实值
    try:
        real_sms_code = redis_store.get("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errcode=RET.DBERR,errmsg="数据库异常")
    # 验证码是否过期
    if real_sms_code is None:
        return jsonify(errcode=RET.NODATA,errmsg="短信验证码已过期")
    
    # 与用户填写的短信验证码进行对比
    if sms_code != real_sms_code:
        # 验证码填写错误
        return jsonify(errcode=RET.DATAERR,errmsg="短信验证码输入不正确")
    
    # 判断手机号是否注册过
    try:    
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errcode=RET.DBERR,errmsg="数据异常")
    else:
        if user is not None:
            # 表示手机号已经存在
            return jsonify(errcode=RET.DATAEXIST,errmsg="手机号以存在")
    
    # 如果相同，表示短信验证码填写正确
    # 对用户的密码进行加密

    #常用的加密算法：md5(不建议使用，已被破解) sha1(不建议使用) sha256   
    # sha256算法：
    #     hashlib.sha256(password).hexdigest()  -->取出加密之后的结果值
    
    #   例如：
    #   user  密码       盐值      加密算法       加密结果
    #    A："123456" + "acevef" -->sha256 -->  sdaabdfef
    #    B："123456" + "fevbfs" -->sha256 -->  sdvsveeve
    
    #    盐值salt：系统随机生成的字符串
    #    如上所示，即使在两个系统中用户的密码一样，但是加密的结果也不一样。

    # 调用werkzeug提供的密码加密方法
    # password_hash = generate_password_hash(password)

    # 将用户数据保存到数据库中
    user = User(
        name = mobile,
        password_hash = "",
        mobile = mobile
    )

    user.generate_password_hash(password)

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        # 表示数据库中存在相同的记录
        return jsonify(errcode=RET.DATAEXIST,errmsg="手机号已经注册过")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errcode=RET.DBERR,errmsg="保存用户信息异常")
        
    # 用session保存登录状态
    session["user_id"] = user.id
    session["user_mobile"] = mobile
    session["user_name"] = mobile
        
        # 返回注册成功的信息
    return jsonify(errcode=RET.OK,errmsg="注册成功",data={"user_id":user.id})
        #'{"errcode":"0","errmsg":"注册成功","data":{"user_id":user.id}}'
