#coding:utf-8
from flask import Flask,current_app

# 创建flask应用核心对象
# app = Flask(模块名)
# __name__表示当前模块的名字
# flask以模板名对应的模块所在的目录为工程目录，默认以目录中的static为静态文件目录，以templates为模板目录
# static_url_path 指明访问静态文件的url前缀
# app = Flask(__name__,static_url_path="/python",static_folder="static",template_folder="templates") -->此处的python是和浏览器中的static对应的
app = Flask(__name__)

# 配置参数的使用
# app.config保存类flask的所有配置信息，我们可以把这个属性当做字典使用
# 方式一：使用文件
# app.config.from_pyfile("config.cfg")

# 方式二：使用对象
class Config(object):
    '''配置参数'''
    DEBUG = True
    NAME = 'LJQ'
app.config.from_object(Config)

# 方式三：当作字典使用
# app.config["DEBUG"] = True 

# 定义视图函数
@app.route("/",methods=['GET','POST'])
def index():
    # n = app.config.get('NAME')
    n = current_app.config.get('NAME')
    print(n)
    return 'hello flask'

# 同一个路径，被不同的视图使用，如果请求方式也相同，则前面定义的会覆盖后面的，
# 如果请求方式不一样，则会冲突；同一个视图函数可以定义多个路径
@app.route('/hello')
def hello1():
    return 'hello1'

@app.route('/hello')
def hello2():
    return 'hello2'

# 同一个视图被多个路径使用方式
@app.route('/h1')
@app.route('/h2')
def hi():
    return 'hi page h1,h2'

if __name__ == '__main__':
    # 启动flask程序
    print(app.url_map)
    app.run(debug=True)
    # app.run(host="192.168.20.81", port=8001)

    