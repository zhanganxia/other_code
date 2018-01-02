day-01
创建flask应用核心对象
app = Flask(模块名)
__name__表示当前模块的名字: app = Flask(__name__)
flask以模板名对应的模块所在的目录为工程目录，默认以目录中的static为静态文件目录，以templates为模板目录
static_url_path 指明访问静态文件的url前缀: app = Flask(__name__,static_url_path="/python")
static_folder:指明静态文件陌路，默认值为static目录
tempalte_folder指明模板目录，默认值为templates
# app = Flask(__name__,static_url_path="/python",static_folder="static",template_folder="templates") -->此处的python是和浏览器中的static对应的


配置参数的使用：
    方式一:使用文件: app.config.from_pyfile('config.cfg') #新建文件config.cfg,文件中写项目的参数哦诶值
    方式二:使用对象: 定义Config的类，在类中保存属性信息，使用方式：app.config.from_object(Config)
    方式三：当作字典使用：app.config保存类flask的所有配置信息，我们可以把这个属性当作字典使用：app.config['DEBUG']=True

调试模式的作用：1.自动重启 2.返回错误信息 

提取配置参数(通过app和current_app都可以提取)：
    从字典中获取：app.config.get('itcast')

指明运行的ip地址，port指明端口(用于在别的终端访问)：
    app.run(host="192.168.20.71",port=8000)

路由的访问方式：
    默认支持以GET方式访问，可以通过methods参数修改支持的访问方式
    @app.route('/',methods=['GET','POST'])
    app.url_map:包含所有的路由信息

同一个路径，被不同的视图使用，如果请求方式页相同，则前面定义的会覆盖后面的，如果请求方式不一样，则会冲突；同一个视图函数可以定义多个路径

路由的重定向：使用url_for来反弹反推路径，url_for接收参数，视图函数的名字

转换器：<转换器类型：参数名字>:@app.route("goods"/<gint:oodss>)
int float path(可以包含/的字符串) 字符串（不能包含/） --默认
@app.route('/goods/<init:goods_id>')
def index(goods_id):
    return 'goods_id=%s'%goods_id

自定义转换器步骤：
    1.以类的方式定义，继承(werzeug.routing模块的 BaseConverter)：
        class MobileConverter(BaseConverter):
            def __init__(self,url_map):
            """
                flask调用的初始化方法，:param url_map:是flask传递的
            """
            #调用父类的初始化方法，将url_map传给父类
            super(MobileConverter,self).__init__(url_map)

            #regex用来保存正则表达式，最终被flask使用匹配提取
            self.regex = r'1[345678]\d{9}'

            def to_python(self,value):
                #我们定义，由flask调用，从路径中提取的参数先经过这个函数的处理，函数的返回值作为视图函数的传入
                return '18211111111'

            def to_url(self,value):
                # 我们定义，由flask调用，在url_for反推路径的时候被调用，用来将处理后的参数添加到路径中
                return '18322222222'

    注意：to_python和to_url方法在有需要的时候去写

    2.向flask添加自定义的转换器：converters包含了flask的所有转换器，可以像字典的方式使用
    app.url_map.converters('moble') = MObileConverter
    
    GET /send_sms/182...665
    flask使用转换器的过程：
        根据转换器的类型名字找到转换器的类，然后实例化这个转换器的对象
        转换器对象中有一个对象属性regex，保存了用来匹配提取正则表达式
    3.使用自定义的转换器
    
        自定义的Converter需要至少定义两个方法：to_python 和to_url
        to_python用于将URL中的路径转换为Python对象，传递给view函数
        to_url则由url_for调用，将参数转换为URL中合适的形式

        @app.route('/send_sms/<mobile:mobile_num>')
        def send_sms(mobile_num):
            return 'send sms to mobile=%s'%mobile_num

        @app.route('/hello')
        def hello():
            url = url_for('send_sms',mobile_name="182***111")

http协议报文：起始行 请求头 Header /r/n 请求体(body)

前端向后端发送参数的方式
    1.从路径中使用正则传参
    2.路径？传参 查询字符串 query string ?a=1&b=2 不限制请求方式，get能传，其他方式也能传
    3.从请求头中传递参数
    4.cookie(在请求头中)
    5.请求体参数：图片、文件、字符串(
        1) 普通表单格式数据："c=3&d=4";
        2) json格式字符串：'{"c":3,"d":2}';
        3) xml格式字符串：'<xml><c>3</c>
                              <d>2</d>
                         </xml>')

postman 接口测试工具