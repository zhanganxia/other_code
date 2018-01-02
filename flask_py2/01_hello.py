#coding:utf-8
from flask import Flask,current_app,redirect,url_for
from werkzeug.routing import BaseConverter #转换器的父类

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

# # 路径的重定向
# @app.route('/login')
# def login():
#     return redirect('/')

@app.route('/login')
def login1():
    # 使用url_for来反推路径url_for接收参数，视图函数的名字
    url = url_for("index")
    print(url)
    return redirect(url)

# 转换器：<转换器类型：参数名字>
@app.route("/goods/<int:goods_id>")
def goodsPage(goods_id):
    return "goods page goods_id=%s" % goods_id

# 自定义转换器
# 1.以类的方式定义
class MobileConverter(BaseConverter):
    """自定义的手机号转化器"""
    def __init__(self,url_map):
        """
        flask调用的初始化方法
        ：param url_map:是flask传递的
        """
        # 调用父类的初始化方法，将url_map传给父类
        super(MobileConverter,self).__init__(url_map)

        # regex用来保存正则表达式，最终被flask使用匹配读取
        self.regex = r'1[34578]\d{9}'

    def to_python(self,value):
        """我们定义，由flask调用，从路径中提取的参数先经过这个函数的处理，函数的返回值作为视图函数的传入参数"""
        return "15994806458"

    def to_url(self,value):
        """我们定义，由flask调用，在用url_for反推路径的时候被调用，用来将处理后的参数添加到路径中"""
        return "18218366567"
# 2.向flask添加自定义的转换器
# converters包含类flask的所有的转换器，可以像字典的方式使用
app.url_map.converters["mobile"] = MobileConverter

# GET /send_sms/186***678  
#根据转换器的类型名字找到转换器的类，然后实例化这个转换器的对象
# 转换器对象中有一个对象属性regex,保存类用来匹配提取的正则表达式
# 3.使用自定义的转换器
@app.route('/send_sms/<mobile:mobile_num>')
def send_sms(mobile_num):
    return "send sms to mobile=%s " %mobile_num

@app.route('/hello3')
def sendMessage():
    url = url_for("send_sms",mobile_num="12345678111") #/send_sms/12345678111
    print('^^^^',url)
    return redirect(url)

if __name__ == '__main__':
    # 启动flask程序
    print(app.url_map)
    app.run(debug=True)
    # app.run(host="192.168.20.81", port=8001)

    