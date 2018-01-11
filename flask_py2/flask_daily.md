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

    删除cookie:delete_cookie("键") 

    max_age="value" -->把cookie的有效期提前


设置session
    使用session模块
    flask中使用session需要配置secret_key参数，否则会报错：
        RuntimeError: the session is unavailable because no secret key was set.
    解决方法(设置secret_key)：
        app.config['SECRET_KEY'] = "qwertyuiop" #随机的字符串

    传统的session保存在数据库中的，flask是直接把session存在cookies中，secret_key的作用就是防止session数据被篡改

    session跨机访问问题

    没有了cookie，session也能实现：将session_id放在路径中

flask上下文
    请求上下文
        request：请求对象，封装了客户端发出的HTTP请求中的内容
        session: 用户会话，用于存储请求之间需要"记住"的值的词典

    程序上下文
        current_app: 当前激活程序的实例
        g：处理请求时，作临时存储的对象。每次请求都会重设这个变量

        全局变量--线程局部变量
        request={
            "线程A"：{"args":{"a":1...}}
            "线程B"：{"args":{"a":2...}}
        }

flask请求钩子(类似与django的中间件二次开发)
    请求钩子使用装饰器实现。
    before_first_request:注册一个函数，在处理第一个请求之前运行
    before_request: 注册一个函数，在每次请求之前运行
    after_request: 注册一个函数，如果没有未处理的异常抛出，则在每次请求之后运行
    teardown_request: 注册一个函数，即使有未处理的异常抛出，也在每次请求之后运行

    注意：在请求钩子函数和视图函数之间共享数据一般使用上下文全局变量g

Flask-Script 扩展命令行
----------------------------------------------------------------------

day-03

Jinja2模板

1.传递模板变量
    render_template(模板路径，模板变量)执行渲染操作
    注意:这里的模板变量和django不同，不是字典格式的，是以"键=值"的形式传递模板变量

    如果要使用类似django的字典传参，在render_template中对字典进行解包"**kwargs"

2.jinja模板获取变量
    直接获取字符串，列表，列表[下标]，字典["key"],字典.key
    在jinja模板中是直接可以进行加法运算：
        1)数字加法:list[1,2]-->{{ list[0] + list[1] }}
        2)字符串加法：name = "python"-->{{ name + "zax" }}

3.模板过滤器
    字符串过滤器
        safe：禁用转义 -->{{ '<em>hello</em>' | safe }}  防止 xss 注入攻击
        capitalize:把变量值的首字母转成大写，其余字母转成小写 -->{{ 'hello' | capitalize }}
        lower:把值转成小写 -->{{ 'HELLO' | lower }}
        upper:把值转成大写 -->{{ 'hello' | upper }}
        title:把值中的每个单词的首字母都转成大写 -->{{  'hello' | title}}
        trim：把值的首尾空格去掉 -->{{ ' hello '| trim }}
        reverse:字符串反转 -->{{ 'olleh' | reverse }}
        format:格式化输出 -->{{ '%s is %d'|format('小明',18) }}
        striptags: 渲染之前把值中所有的HTML标签都删除掉 -->{{ '<em>hello</em>'| striptags }}

    列表过滤器
        first:取第一个元素-->{{ [1,2,3,4] | first }}
        last:取最后一个元素-->{{ [1,2,3,4] | last }}
        length:获取列表长度-->{{ [1,2,3,4] | length }}
        sum:列表求和-->{{ [1,2,3,4] | sum }}

    flask支持链式使用过滤器
        一个模板变量可以添加多个过滤器进行处理-->{{ ' hello ' |trim|upper }}
    
    自定义过滤器
        方式一：通过add_template_filter(过滤器函数，模板中使用的过滤器)
                ----------------------------------------------------------
                def filter_double_sort(ls):
                return ls[::2]
                app.add_template_filter(filter_double_sort,'double_2')
                ----------------------------------------------------------

        方式二：通过装饰器 app.template_filter(模板中使用的装饰器名字)
            ------------------------------------------------------------
            @app.template_filter('db3')
            def filter_double_sort(ls):
                return ls[::-3]
            ------------------------------------------------------------

4.控制语句和宏
    控制语句：
        {% if %}{% endif %} 
        {% for item in samples %}{% endfor %}
    宏：
        宏：在模板中重复使用的代码块(和python中的函数类似)
        宏的定义：{% macro 函数 %} 重复的代码块 {% endmacro %}
        宏的使用：{{ 宏的函数名 }}
        宏函数可以定义带参数的和不带参数的：
        带参数的宏的使用方法：
            定义：{% macro input(name,type='text') %}
                    <input name={{ name }} type={{ type }}>
                {% endmacro %}
            使用： {{ input('python') }}
        
        使用其他文件中定义的宏(需要导入调用)：
            {% import 'macro_input.html' as m_input %}
            {{ m_input.input() }}

5.表单 - WTForm
    使用Flask-WTF表单扩展，可以帮助进行CSRF验证，帮助我们快速定义表单
    注意：使用wtform扩展，需要配置secret_key：app.config["SECRET_KEY"] = "aaaasssddd"
    使用表单的流程：
        1）定义表单（from flask_wtf import FlaskForm）
        -----------------------------------------------------------
        class RegisterForm(FlaskForm):
            '''注册表单'''
            # validators指明对这个字段的验证行为
            user_name = StringField(label=u"用户名",validators=[DataRequired(u'用户名不能为空')])
            password = PasswordField(label=u"密码",validators=[DataRequired(u"密码不能为空")])
            password2 = PasswordField(label=u"重复密码",validators=[DataRequired(u"确认密码不能为空"),EqualTo("password",u"两次密码不一致")])
            submit = SubmitField(label=u"提交注册")
        ------------------------------------------------------------

        2）创建表单对象
        -----------------------------------------------------------
        @app.route("/register")
        def register():
            # 创建表单对象
            form = RegisterForm()
            return render_template("hello3.html",form=form)
        -----------------------------------------------------------

        3）传入模板，在模板中直接操作对象
        ----------------------------------------------------------
        <form method="post">
        <p>{{ form.user_name.label }}</p>
        <p>{{ form.user_name }}</p>
        <!--  -->
        {% for err in form.user_name.errors %}
        <p>{{ err }}</p>
        {% endfor %}
        </form>

        模板中传入csrf_token
        {{ form.csrf_token }}:表单对象传给模板的form中有一个csrf_token的属性

6.代码的重用
    include：将另一个模板加载到当前模板中，并直接渲染，包含在使用时，如果包含的模板文件不存在，程序会抛出TemplateNotFound异常，使用ignore missing关键字，如果包含的模板文件不存在，会忽略这条include语句

    宏，继承，包含：
        宏(Macro),继承(Block),包含(include)均能实现代码的复用
        继承(Block)的本质是代码替换，一般用来实现多个页面中重复不变的区域
        宏(Macro)的功能类似函数，可以传入参数，需要定义，调用
        包含(include)是直接将目标模板文件整个渲染出来

7.Flask中的特殊变量和方法
    在Flask中，有一些特殊的变量和方法，是可在模板文件中直接访问的
    config对象：app.config对象
    request对象：当前请求的request对象
    url_for()方法：返回传入的路由函数对应的URL，将参数做为命名参数使用

    闪现flash：
        在视图模块引入flash-->保存闪现要展示的消息数据-->flash(消息数据)
        在模板中：get_flashed_messages()：获取flash()传入的消息数据
        一次保存的数据只能在模板中提取一次，再次提取就没有了
        flask在实现闪现的时候，是将flask的数据保存到session中，
        使用flash需要保证程序中有配置过secret_key的参数

8.数据库

-----------------------------------------------------------------
day-04

数据库迁移扩展的使用
    创建启动命令工具对象：manager = Manager(app)
    初始化Migrate迁移工具：Migrate(app,db)
    向启动命令工具中添加数据库迁移工具：manage.add_command=("db",migrateCommand)
    执行对应的初始化操作：python db.py db init
    生成迁移文件：python db.py db migrate
    添加备注信息：python db.py db migrate -m"备注"
    将迁移文件同步到数据库：python db.py db upgrade    
    查看数据库的迁移历史：python db.py db history

邮件扩展：Flask-Mail
    邮箱的配置在：app.config(字典)中添加，使用其内建方法update
    配置的信息：

蓝图Blueprint
    flask app对象代表整个项目
    蓝图作用：
    循环导入：A导B，B导A，互相僵持，类似于死锁

    蓝图的使用步骤：
        创建蓝图对象：app_users=Blueprint("app_users",__name__)
        定义蓝图的所有视图
        把
        url_prefix指明访问蓝图路由的路径前缀

        蓝图需指明那个是静态文件目录，那个是模板文件目录

单元测试
    断言：assert
    常用的断言方法：
    isinstance

    单元测试代码编写流程：
        a.向登录接口发送请求
            方式一，万能方式：
            urllib urllib2 requests http客户端

            方式二，使用框架的测试客户端
            flask的测试客户端：client = app.test_client -->相当于postman接口测试工具
            发起post请求，返回响应对象
            response = client.post('后端接口路径',请求体数据)            
        b. 接收接口的响应信息
            获取响应体数据：json_str = response.data
            resp_dict = json_str.loads(json_str)
        c.判断响应信息是否符合我们的预期
            self.assertIn("code",resp_dict)

    测试代码执行前和收尾函数
        setUp()-->在执行所有的测试方法前，先被调用,将单元测试代码中重复代码可以放在此方法中
        tearDown()-->在所有的测试方法执行后，被调用，用来收尾清理操作

    设置flask的测试模式
        app.config["TESTING"] = True
        如果被测试的flask程序出现类异常，可以在单元测试中反应出异常信息
        
部署
    gunicorn 绿色独角兽  pip install gunicorn
       
        gunicorn -w 4 -b 127.0.0.1:5000 main:app
        参数：-w:进程（worker）
             -b:ip地址和端口号(bind)

        后台程序运行 脱离终端 -D
        gunicorn -w 4 -b 127.0.0.1:5000 -D main:app     
        退出进程：kill -9 27539 -->杀主进程

        --access-logfile:
         gunicorn -w 4 -b 127.0.0.1:5000 --access-logfile main:app 


--------------------------------------------------------------
ady-05 微信开发

微信生成签名
    对要转发的数据与token一起进行计算，得到签名

认证签名
    从请求的数据中取出签名，计算需要的数据，连同token一起计算的计算后的签名值，与请求中的签名值对比，如果相同，证明请求来自微信

必须运行在公网ip地址：80/wechat

接入微信配置与token参数说明
    token:令牌（随机字符串），信赖谁就给谁
    签名数据：对要转发的数据与token一起进行计算，得到签名
    验证签名：从请求的数据中取出签名，计算需要的数据，连同token一起计算的，极端后的签名值，与请求中的签名值对比，如果相同，证明请求来自微信，否则非法请求

    公网ip地址：80/wechat8012

微信测试服务器
    ip:101.200.170.171:80
    帐号：s80xx s8012
    密码：123456a
    url:http://101.200.170.171/wechat8012
    token:自己指定
    
    开发程序：@route("/wechate80xx")
        app.run(port=80xx)

    登录服务器-->创建自己的文件夹，将本地的wechat.py远程推送到远程服务器( scp ./wechat.py s8012@101.200.170.171:~/wechat_zax/)-->在远程服务器中选择一个flask虚拟环境-->在虚拟环境中运行wechat.py

验证服务器地址的有效性
    开发者提交信息后，微信服务器将发送GET请求到填写的服务器地址URL上，GET请求携带的四个参数：
    signature: 微信加密签名，signature结合了开发者填写的token参数和请求中的timestamp参数、nonce参数
    timestamp: 时间戳
    nonce：随机数
    echostr: 随机字符串

开发者通过校验signature对请求进行校验
    校验流程：
        1）将token、timestamp、nonce三个参数进行字典序排序
        2）将三个参数字符串拼接成一个字符串进行sha1加密
        3）开发者获得加密后的字符串可与signature对比，标识该将请求来源于威信
    
    代码
    ------------------------------------------------------------------------------------------------------------
    #encoding=utf-8
    import time
    from flask import Flask,request,abort
    import hashlib  #python标准库，里面提供sha1 md5 sha256等加密方法
    import xmltodict

    WECHAT_TOKEN = "itcast" #常量

    app = Flask(__name__)

    # 第一请求：是微信服务器发起的验证请求
    # GET /wechat
    @app.route("/wechat8012",methods=["GET","POST"])
    def wechat():
        '''处理微信公众号的请求'''
        # 验证请求是否来自微信
        signature = request.args.get("signature")
        timestamp = request.args.get("timestamp")
        nonce = request.args.get("nonce")

        # 按照微信指明的方式，计算签名值
        # 1. 将token，timestamp,nonce三个参数进行字典排序
        li = [WECHAT_TOKEN,timestamp,nonce]
        li.sort()

        # 2.将三个参数字符串平成一个字符串
        tmp_str = "".join(li)

        # 3.进行sha1加密计算
        hash_obj= hashlib.sha1(tmp_str)
        sign = hash_obj.hexdigest()#获取计算后的结果

        # 4.对比自己计算的sign值与请求中的signature值，如果相同，证明请求成功
        if sign != signature:
            # 表示请求不是微信
            abort(403)        
        if request.method == "GET":
            
            # 按照微信的说明，为了响应微信的验证请求，需要把微信请求中的
            echostr = request.args.get("echostr")
            return echostr
        else:
            # post
            # 获取请求体xml消息数据
            xml_str = request.data
            # 解析xml
            xml_dict = xmltodict.parse(xml_str)
            req_dict = xml_dict["xml"]

            # 取出消息类型
            msg_type = req_dict["MsgType"]

            if msg_type == "text":
                # 表示文本类型消息
                # 构造回复的消息
                resp_dict = {
                    "xml": {
                        "ToUserName":req_dict.get("FromUserName"),
                        "FromUserName":req_dict.get("ToUserName"),
                        "CreateTime":int(time.time()),
                        "MsgType":"text",
                        "Content":req_dict.get("Content")
                    }
                }
            else:
                resp_dict = {
                    "xml": {
                        "ToUserName":req_dict.get("FromUserName"),
                        "FromUserName":req_dict.get("ToUserName"),
                        "CreateTime":int(time.time()),
                        "MsgType":"text",
                        "Content":"hello welcome!"
                    }
                }
                
            # 决定返回的xml数据
            xml_resp_str = xmltodict.unparse(resp_dict)
            return xml_resp_str            
    if __name__ == '__main__':
        app.run(port=8012,debug=True)
    --------------------------------------------------------------------------------------------------

微信网页授权获取用户基本信息
    流程：
    第一步：用户同意授权，获取code(授权书)
    第二步：通过code换取网页授权access_token(微信服务器访问令牌)
    第三步：拉取用户信息(需scope为snaspi_userinfo)


    xmltodict模块：可以把xml字符串转化为python中的字典

    http://101.200.170.171/wechat8012

    1.在微信中配置域名：www.itcastcpp.cn

    http://101.200.170.171/wechat8012/index
    http://www.itcastcpp.cn/wechat8012/index

    2.将网址转换
    urllib.quote("http://www.itcastcpp.cn/wechat8012/index")
    转换后：http%3A//www.itcastcpp.cn/wechat8012/index

    3.用户访问地址
    https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxa401712a4f50cc75&redirect_uri=http%3A//www.itcastcpp.cn/wechat8012/index&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect
        用在线二维码生成器生成上面这个链接地址的二维码信息，用手机扫描，进行授权

    代码 
    ————————————————————————————————————————————————————————————————————————————————————————————————————————
    web_page:
        #encoding=utf-8
        from flask import Flask,request,render_template
        import urllib2
        import json

        WECHAT_APPID = "wxa401712a4f50cc75"
        WECHAT_SECRET = "e0f5cd4b2a1c793f9760b9a5a7f26ccc"

        app = Flask(__name__)

        # GET /wechat8012/index?code=xxx
        @app.route("/wechat8012/index")
        def index():
            # 获取code参数
            code = request.args.get("code")
            # 获取access_token
            url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code"%(WECHAT_APPID,WECHAT_SECRET,code)
            
            # 使用urllib2发起请求,返回响应对象
            response = urllib2.urlopen(url)

            # 读取响应体的数据
            json_str = response.read()
            resp_dict = json.loads(json_str)

            if "errcode" in resp_dict:
                # 表示微信出错
                return "获取access_token失败"
            access_token = resp_dict.get("access_token")
            user_openid = resp_dict.get("openid")

            # 获取用户的数据
            url = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN"%(access_token,user_openid)
            
            # 使用urllib2发起请求,返回响应对象
            response = urllib2.urlopen(url)

            # 读取响应体的数据
            json_str = response.read()
            resp_dict = json.loads(json_str)

            if "errcode" in resp_dict:
                # 表示微信出错
                return "获取用户数据失败"
            # 获取用户数据成功
            return render_template("index.html",user=resp_dict)

        if __name__ == '__main__':
            app.run(port=8012,debug=True)
    *************************************************************************
    templates/index.html:
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{{user["nickname"]}}的个人主页</title>
        </head>

        <body>
            <img alt="头像" src="{{user['headimgurl']}}" width="60">
            <table>
                <tr>
                    <th>openid</th>
                    <td>{{user["openid"]}}</td>
                </tr>
                <tr>
                    <th>昵称</th>
                    <td>{{user["nickname"]}}</td>
                </tr>
                <tr>
                    <th>性别</th>
                    <td>
                        {% if 1 == user["sex"] %} 男 {% elif 2 == user["sex"] %} 女 {% else %} 未知 {% endif %}
                    </td>
                </tr>
                <tr>
                    <th>省份</th>
                    <td>{{user["province"]}}</td>
                </tr>
                <tr>
                    <th>城市</th>
                    <td>{{user["city"]}}</td>
                </tr>
                <tr>
                    <th>国家</th>
                    <td>{{user["country"]}}</td>
                </tr>
            </table>
        </body>
        </html>
    _________________________________________________________________________________________________________
    

-----------------------------------------------------------------
day-06 flask项目

前后端分离和不分离的比较：
    前后端不分离：前端看到页面的内容是从后端处理完成的结果传递给前端的(前端看到的页面内容是后端处理的结果)对SEO优化友好(搜索引擎优化)
    前后端分离：后端只提供数据，不负责前端页面处理。(无论前端是网页还是app都可以达到后端的复用)网页前端采用ajax请求，对SEO优化不友好

以单一文件构建项目的所有工具
    -.导入flask_script的Manager模块(使用：；python xxx.py runserver)
        添加启动命令扩展:manager = Manager(app),使用manager启动程序
    -.添加配置信息(两种方式：类的方式，单一文件方式)，此处使用类的方式.
        class Config(object):
            DEBUG = True
            SECRET_KEY = "ADSGJKKGFFAADadsf"

            #数据库
            SQLALCHEMY_DATABASE_URL="数据库类型://用户名：密码@本地IP：端口/数据库名"  #数据库配置信息
            SQLALCHEMY_TRACK_MODIFICATIONS = True #Flask-SQLAlchemy 将会追踪对象的修改并且发送信号，默认为True

            #redis
            REDIS_HOST = "127.0.0.1"
            REDIS_PORT = 6379
            REDIS_DB = 0

            #session的配置信息
            SESSION_TYPE = "redis" #指明session数据保存在redis中
            SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT,db=1)#使用redis数据库 
            SESSION_USE_SIGNER = True #指明对cookie中保存的session_id进行加密防护
            PERMANENT_SESSION_LIFETIME = 3*24*60*60 #session有效期，单位秒

        #1.添加flask配置
        app.config.from_object(Config)
        
        #2.创建数据库工具，从flask_sqlalchemy导入模块SQLAlchemy
        db = SQLAlchemy(app) 

        #3.初始化迁移工具，从flask_migrate导入：Migrate,Migratecommand
        Migrate(app,db)

        #4.添加数据库迁移命令
        manager.add_command("db",Migratecommand)

        #5.创建redis链接实例，并接收，使用导入模块redis
        redis.StrictRedis(host=Config.REDIS_HOST,port=xxx,db=xxx)

        #6.配置session，引入扩展flask_session,对session进行初化
        Session(app)

        #7.补充csrf防护
        #flask_wtf 表单扩展(有实现csrf_token,但是未实现前后端的分离)，csrf防护是这个扩展的组成部分，可以直接使用csrf而不使用表单

    补充：
    csrf的防护机制：
        对于包含了请求体的请求(POST,PUT,DELETE),从请求的cookie中读取一个csrftoken的值,从请求体中读取一个csrf_token的值，进行比较，如果相同则允许访问，否则返回403的错误
        csrf在flask_wtf中是通过请求钩子的方式添加上来的

    flask模块session和flask_session中Session的比较
        from flask import session -->从flask中导入操作session对象
        from flask_session import Session  -->从扩展工具导入Session的初始化的类，这个扩展工具改变了flask默认存储session的位置(不再存储在cookie中，而是可以自己选择)

        在配置此扩展类的时候需要添加secrit_key="任意字符"，用于cookie中保存的session_id进行加密保护

项目目录的拆分

    config.py: 项目开发环境的配置信息
        以类的方式保存项目的配置信息，优点：多个开发环境(测试、集成、线上)时可以达到配置信息的复用

        开发环境的分离，不同的开发环境继承相同配置信息的Config类
    
    工厂模式：对外隐藏对象的构建过程，仅提供工厂函数

    其他：
        根据版本号拆分视图

        绝对路径以启动目录做为思考

        循环导入，解决方法-->延迟导入，什么时候用什么时候导

utils 目录（utility）存放自己实现的通用共用组件（函数，类，模块）
libs 目录（library）存放：第三方(别人)开发的工具包（函数，类，模块） 完整的库

6.日志 logging(python的标准日志模块)
    flask使用日志
        app.logger() 记录日志信息
        current_app.logger

    日志等级:
        error 错误   --   current_app.logger.error("数据库发生异常")
        warning 警告级别 -- current_app.logger.warning()
        info 通知信息  --   current_app.logger.info()
        debug 调试   --    current_app.logger.debug()

        error日志等级最高，debug日志等级最低
            设置日志记录等级为debug，日志中会记录：debug,info,warning,error信息
            设置日志记录等级为info，日志中会记录：info,warning,error信息
            设置日志记录等级为warning，日志中会记录：warning和error信息
            设置日志记录等级为error，日志中仅会记录error信息，不会记录warning,info,debug信息

    日志的配置信息：
        # 设置日志的记录等级
        logging.basicConfig(level=logging.DEBUG)  # 调试debug级

        # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
        file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)

        # 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
        formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')

        # 为刚创建的日志记录器设置日志记录格式
        file_log_handler.setFormatter(formatter)

        # 为全局的日志工具对象（flask app使用的）添加日记录器
        logging.getLogger().addHandler(file_log_handler)

数据库的迁移
        pip install flask-migrate
    创建迁移仓库： python manage.py db init  -->创建migrations文件夹，所有迁移文件都放在里面

    创建迁移脚本：python manage.py db migrate -m 'initial migration'

    更新数据库： python database.py db upgrade

    回退数据库： python database.py db downgrade 版本号

        
 --------------------------------------------------------------------

day-07 

联合主键：      
转换器 
自定义转换器的流程？
current_app.send_static_file(文件名) 
csrf_token 在django和flask中设置的区别？
设置cookie?
    from flask_wtf import csrf
    make_response(文件名)
    # 生成csrf_token随机字符串的值
    csrf_token = csrf.generate_csrf()

    # 设施csrf用到的cookie
    resp.set_cookie("csrf_token",csrf_token)

浏览器同源策略：不同源的网站不能相互操作资源
    判断同源：网站域名+端口号+协议

图片验证码的流程？

Restful风格？
    goods
    不符合风格：
        /get_goods
        /save_goods
        /update_goods

    符合风格：
        /goods 路径中只出现名词，表示操作的数据资源
        使用HTTP的不同请求方式来对应增删改查四种操作

        GET /goods 查询商品数据
        POST /goods 保存一个商品数据
        PUT /goods 新建一个商品数据
        DELETE /goods 删除一个商品数据

自定义响应头？

UUID 通用唯一识别码(全局唯一标识符) -- 在前端中生成验证码图片ID
时间戳

        



