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
    方式一:使用文件: app.config.from_pyfile('config.cfg') #新建文件config.cfg,文件中写项目的参数和值：DEBUG=True

    方式二:使用对象: 定义Config的类，在类中保存属性信息，使用方式：app.config.from_object(Config)
    方式三：当作字典使用：app.config保存类flask的所有配置信息，我们可以把这个属性当作字典使用：app.config['DEBUG']=True

调试模式的作用：1.自动重启 2.返回错误信息 
调试模式的启用方式：
    1.直接在应用对象上设置； app.debug=True
    2.作为run方法的一个参数传入:app.run(debug=True)

提取配置参数(通过app和current_app都可以提取)：
    从字典中获取：app.config.get('itcast')

指明运行的ip地址，port指明端口(用于在别的终端访问)：
    app.run(host="192.168.20.71",port=8000)

路由的访问方式：
    默认支持以GET方式访问，可以通过methods参数修改支持的访问方式
    @app.route('/',methods=['GET','POST'])
    app.url_map:包含所有的路由信息

同一个路径，被不同的视图使用，如果请求方式也相同，则前面定义的会覆盖后面的，如果请求方式不一样，则会冲突；同一个视图函数可以定义多个路径

路由的重定向：使用url_for来反弹反推路径，url_for接收参数，视图函数的名字

转换器：<转换器类型：参数名字>:@app.route("/goods/<int:goods_id>")
    常见的转换器的类型：
        int 接受整数  
        float同int,但是接受浮点数  
        path和默认的相似，也接受斜线


int float path(可以包含/的字符串) 字符串（不能包含/） --默认
@app.route('/goods/<goods_id>')#默认是字符串类型
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
    5.请求体参数：图片、文件、（多媒体表单）
        字符串(
        1) 普通表单格式数据："c=3&d=4";
        2) json格式字符串：'{"c":3,"d":2}';
        3) xml格式字符串：'<xml><c>3</c>
                              <d>2</d>
                         </xml>')

postman 接口测试工具
接口：让别人访问的api


-------------------------------------------------------------
day-02

json字符串中键的引号必须是双引号
raw 原始


flask获取请求数据：
    1.获取查询字符串的数据：
        a = request.args.get("a") -->获取同名参数的一个值
        a_list = request.args.getlist("a") -->获取所有的同名参数

    2.获取请求头数据：content_type = request.headers.get("Content-Type")
    
    3.获取请求体的数据:
        1) 普通表单格式的字符串：c = request.form.get("c")
        2）获取所有同名表单格式的字符串：d = request.form.getList("list")
    
    4.获取json格式的字符串
        request.data中包含了最原始的请求体数据

        json字符串在python中的处理

            python中标准模块 json
            json字符串 --> python中的字典 json.loads(json字符串) --> 返回字典数据

            python中的字典 --> json字符串 json.dumps(python中的字典)  --> 返回json字符串

            请求头Content-Type是application/json时，使用postman接口测试工具测试接口时，需要在Header中指明Content-Type
        
        flask获取json格式串的两种方法:
            方式一：如果请求头中Context-Type不是application/json,通过请求原始数据的方式请求数据：request.data
                json_str = request.data
            方式二：如果请求头中Context-Type是application/json，通过简便的方式请求数据：get_json(会将请求体的json字符串直接转换为字典返回给我们)
                json_dic = request.get_json()

    5.保存文件数据
        通过files属性获取文件数据，返回文件对象：
        files_obj = request.files.get("pic")

        方式一：自己手动保存
            read方法读取文件内容-->获取上传文件的真实名字-->在本地创建打开一个新文件(with open(路径,读写方式) as new_file:)-->写入新文件

        方式二：使用save方法
            files_obj.save("./"+files_obj.filename)        

        多媒体表单用html实现方式：
            在表单声明中添加：enctype="multipart/form-data"属性
            <form method="post" enctype="multipart/form-data">
                <input type="file" name="pic">
            </form>

python2与python3字符串的区别
    python3 类型 str
    python2 类型 unicode --> u"a" 
                str --> "a"

    python2中容易出现的错误：
    错误提示信息：ascii cannot decode \xd3\xde
    表示：程序中的字符串数据出现类非英文字符
    出处：字符串格式化处理的时候
    原因：用了str类型与unicode类型，两种不同的类型进行字符串处理，print("参数a=%s"%s)python都是转换为unicode类型再处理，默认以ascii编码来解读非英文字符
    解决方法：对于非英文字符串声明的时候就声明为unicode类型 如：u"参数a=%s"

    ascii只对英文字符编码

能包含请求体的方法：POST PUT DELETE
pycharm 快速导包 alt+enter

abort函数的使用
    abort函数在flask模块中
    abort()函数可以立即终止视图函数的执行，并向前端返回"标准的"指定的错误状态码：abort(错误状态码) 400-->错误的请求  403-->禁止访问

自定义处理错误的页面
    用app.errorhandler(状态码)装饰器装饰
    自定义的处理404错误的方法，e被flask调用的时候，传入的错误的对象
    def handler_404(e):
        return e

构造响应信息的方式:
    方式一:元组  
        return (响应体，状态码，响应头) -->加不加括号都可以
        return 响应体，状态码，响应头(列表，字典)
        return "index page",403,[(响应头的名字,响应头的值),()...]

    方式二：make_response()
        res = make_response(响应体) -->返回响应对象
        res.status = "状态码"
        res.headers['name'] = 'python3'

jsonify ==>等价与django的jsonResponse,把数据转换为json字符串返回，并帮助我们设置响应头Content-Type为application/json

设置和读取cookie
    设置cookie 通过make_response获取resp对象，resp.set_cookie(名字，cookie值)-->设置cookie
    默认是临时cookie，浏览器关闭即失效
    通过max_age指明有效期，单位是秒

    获取cookie:request.cookies.get("键")

    删除cookie:delete_cookie("键") -->把cookie的有效期提前


设置session
    使用session模块
    flask中使用session需要配置secret_key参数，否则会报错：
        RuntimeError: the session is unavailable because no secret key was set.
    解决方法(设置secret_key)：
        app.config['SECRET_KEY'] = "qwertyuiop" #随机的字符串

session跨机访问问题

没有了cookie，session也能实现：将session_id放在路径中

全局变量--线程局部变量
