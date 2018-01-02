#coding:utf-8
from flask import Flask

# 创建flask应用核心对象
# app = Flask(模块名)
# __name__表示当前模块的名字
# flask以模板名对应的模块所在的目录为工程目录，默认以目录中的static为静态文件目录，以templates为模板目录
# static_url_path 指明访问静态文件的url前缀
# app = Flask(__name__,static_url_path="/python")
app = Flask(__name__)

# 定义视图函数
@app.route("/")
def index():
    return 'hello flask'

if __name__ == '__main__':
    # 启动flask程序
    app.run()
    