#encoding=utf-8

from flask import Blueprint
from flask import current_app

html = Blueprint("html",__name__)

# GET 127.0.0.1：5000/要访问的html文件名
@html.route('/<re(r".*"):file_name>')
def get_html_file(file_name):
    """提供静态的html文件资源"""
    # 从请求的路径中提取html文件名，去html目录中找到文件并返回给用户
    # send_static_file(静态目录中的文件名)，函数会自动去静态目录中找文件，返回包含文件内容的响应信息

    if not file_name:
        file_name = "index.html"
    
    file_name = "html/" + file_name

    return current_app.send_static_file(file_name)
    

