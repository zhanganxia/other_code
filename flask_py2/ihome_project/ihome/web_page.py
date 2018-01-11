#encoding=utf-8

from flask import Blueprint,make_response
from flask import current_app
from flask_wtf import csrf

html = Blueprint("html",__name__)

# GET 127.0.0.1：5000/要访问的html文件名
# 浏览器自动发送的请求 GET 127.0.0.1:5000/favicon.ico -->网站的logo


@html.route('/<re(r".*"):file_name>')
def get_html_file(file_name):
    """提供静态的html文件资源"""
    # 从请求的路径中提取html文件名，去html目录中找到文件并返回给用户
    # send_static_file(静态目录中的文件名)，函数会自动去静态目录中找文件，返回包含文件内容的响应信息

    if not file_name:
        file_name = "index.html"

    if file_name != "favicon.ico":
        
        file_name = "html/" + file_name

    resp = make_response(current_app.send_static_file(file_name))

    # 生成csrf_token随机字符串的值
    csrf_token = csrf.generate_csrf()

    # 设施csrf用到的cookie
    resp.set_cookie("csrf_token",csrf_token)

    return resp
    

