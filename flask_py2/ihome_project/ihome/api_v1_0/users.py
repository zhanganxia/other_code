#encoding=utf-8
from . import api
from ihome import db
from flask import current_app

@api.route('/register')
def register():
    # 记录日志
    current_app.logger.error("错误级别信息")
    current_app.logger.warning("警告级别信息")
    current_app.logger.info("信息级别信息")
    current_app.logger.debug("调试级别信息")
    
    return "register page"