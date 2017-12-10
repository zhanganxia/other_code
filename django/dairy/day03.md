URLconf
1. URL配置过程
    1.1 settings.py中，指定入口urls文件（项目创建时自动配置的）
        ROOT_URLCONF = '项目.urls'

    1.2 在项目中urls.py中，包含到应用的urls.py
        url（正则，include('应用.urls')）

    1.3 应用中urls.py中，调用views.py对应的函数
        url(正则，views.函数名)

2. URL函数
    2.1 url函数有两个参数，第一个参数是正则表达式，第二个是对应的处理动作。配置url时，有两种语法格式：
        a)url(正则表达式，视图函数名)
        b)url(正则表达式，include(应用中的urls文件))

3. URL的匹配过程
    3.1 用户在浏览器输入网址，请求django服务器
    3.2 settings文件中的ROOT_URLCONF定义的urls文件
    3.3 应用中的urls文件
    3.4 调用views文件中的render函数

4. 正则书写规则
    a. 推荐使用r，表示字符串不转义
    b. 不能在开始加反斜杠，因为在截取url时会自动去掉前面的反斜杠再和正则匹配，如果在正则前面加反斜杠就匹配不上了

5. URL中取值
    如果想从URL中获取值，需要在正则表达式中使用分组，获取值分为两种方式
    5.1 位置参数 参数的位置不能错
        例：http://127.0.0.1:8000/18/188/，提取出18  188
        urls配置：
            url(r'^(\d+)/(\d+)/$'),views.index)

        视图views.py中的配置：
            def index1(request,value1,value2):
            context = {'v1':value1,'v2':value2}
            return render(request,'booktest/index.html',context)
        在html页面显示获取的值：<h3>{{v1}} {{v2}}</h3>
        
    5.2 关键字参数（parameter） 参数的位置可以变,跟关键字保持一致即可
        urls配置：
            url(r'^(?P<parameter1>\d+)/(?P<parameter2>\d+)/$',views.index2)
        
        视图views.py中的配置
            def index2(request,parameter1,parameter2):
            context1 = {'val01':parameter1,'val02':parameter2}
            return render(request, 'booktest/index.html',context1)

    注意：
        1.两种参数的方式不要混合使用，在一个正则表达式中只能使用一种参数方式
        2.同一URL使用两种匹配方式去匹配，写在前面的会匹配成功，后面的匹配就不会执行了
        例如：以下两种方式一起匹配：http://127.0.0.1:8000/18/188/ 方式二就不会执行了，因为方式一已经匹配成功了

            方式一： url(r'^(\d+)/(\d+)/$',views.index1),
            方式二：url(r'^(?P<parameter1>\d+)/(?P<parameter2>\d+)/$',views.index2),

6. 错误视图
    Django内置处理HTTP错误的视图，主要错误及视图包括：
        404错误：URL匹配不成功 page not found视图
        400错误：客户端的安全方面非法操作（篡改cookie） bad request视图
        500错误：代码运行报错会发生500错误 server error视图

    只需要在模板中定义指定html文件即可(在templates文件夹下一级目录即可)，不需要配置URL和准备视图，要想看到错误视图还需修改setting文件中的：
        DEBUG = False
        ALLOWED_HOSTS = ['*',]

7. HttpRequest对象
    服务器接收到http协议的请求后，会根据报文创建HttpRequest对象，这个对象不需要我们创建，直接使用服务器构造好的对象使用
    视图的第一个参数必须是HttpRequest对象
    在django.http模块中定义了HttpRequest对象的API，使用HttpRequest对象的不同属性值，可以获取请求中多种信息

    属性：
        path: 一个字符串，表示请求的页面的完整路径
        method: 一个字符串，表示请求使用的HTTP方法 ‘GET’ 'POST'
        encoding：一个字符串，表示提交的数据的编码方式
        
        GET：一个类似与字典的对象，包含get请求方式的所有参数
        POST：一个参数类似于字典的对象，包含post请求方式的所有参数
        FILES: 一个类似于字典的对象，包含所有上传的文件
        COOKIES：一个标准的Python字典，包含所有的cookie，键和值都是字符串
        SESSION：一个既可读又可写的类似于字典的对象，表示当前的会话，只有当Django 启用会话的支持时才可用

    7.1.QueryDict对象
        . QueryDict对象定义在django.http.request中，HttpRequest对象的GET、POST属性都是QueryDict类型的对象（重要）
        . QueryDict类型的对象不是字典，仅仅是类似字典的对象而已
        . 与标准的python字典不同，QueryDict类型的对象可以用来处理同一个键带有多个值的情况
        . QueryDict类型的对象，键和值都是字符串的类型
        . 键是开发人员在编写代码时确定下来的，值是根据数据生成的

        get()方法：根据键获取值，如果一个键同时拥有多个值将获取最后一个值，如果键不存在则返回None值，可以设置默认值进行后续处理

        getlist()方法：根据键获取值，值以列表返回，可以获取指定键的所有值，如果键不存在则返回空列表[]


MIDDLEWARE_CLASSES  中间件
'django.middleware.csrf.CsrfViewMiddleware', 设置跨站请求CSRF伪造保护

    

    
