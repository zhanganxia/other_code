1. 框架
    MVC架构
        M：模型  
        V：视图
        C：控制器  接收请求和数据进行处理

    Django MVT架构
        M：模型  读写数据库
        V：视图  接收请求，与M和T交互，再返回应答
        T：模板（Template） 提供HTML模板

    分模块目的：解耦  降低代码之间的关联


2. 环境(虚拟环境)
    虚拟环境的作用：虚拟环境可以为每个项目搭建独立的python运行环境，使得每个项目依赖的python环境独立

    2.1 安装虚拟环境包
        sudo pip install virtualenv
        sudo pip install virtualenvwrapper

        virtualenv：是一个可以在同一计算机中隔离多个python版本的工具
        virtualenvwrapper：是virtualenv的扩展管理包，用于更方便管理虚拟环境
                          作用：
                            1.将所有虚拟环境整合在一个目录下
                            2.管理（新增，删除，复制）虚拟环境
                            3.切换虚拟环境

    2.2 设置虚拟环境默认生成地址
        编辑当前用户家目录下的.bashrc文件
        添加配置：
        export WORKON_HOME=$HOME/virtualenvs  -->设置虚拟环境存放目录
        source /usr/bin/virtualenvwrapper.sh  -->添加virtualenvwrapper路由。注意：用户不同，此路径需要变更

        使用source .bashrc使其生效

    
    2.3 创建虚拟环境
            python2: mkvirtualenv <虚拟环境名称>
            python3: mkvirtuallenv -p python3 <虚拟环境名称>
    
    2.4 虚拟环境操作命令：
        查看和使用虚拟环境： 
            workon 按两次tab  -->查看所有虚拟环境
            workon 虚拟环境名称(按tab键可以补齐) -->选择使用哪个虚拟环境

        退出虚拟环境： deactivate

        删除虚拟环境：先退出虚拟环境，然后再删除
            deactivate  退出虚拟环境
            rmvirtualenv py_django  删除虚拟环境

    2.5 虚拟环境下安装包
        pip install 包的名称
        安装Django包： pip install django==1.8.2
        显示所有的安装包：pip list

3. 创建项目
    3.1创建项目准备
        workon py_django 进入虚拟环境
        cd /项目存放目录
        mkdir pytest
        cd pytest
    3.2创建项目（名称为test1）
        django-admin startproject test1

        项目目录说明：
        __init__.py:让python把该目录当成一个开发包（即一组模块）所需要的文件。这是一个空文件一般不需要修改
        manage.py: 是项目运行的入口文件和管理文件。补充：一种命令行工具，允许你以多种方式与该Django项目进行交互
        项目配置包，与项目同名，所有的项目配置都在这里
        init.py: 是一个空的文件，作用是这个目录test1可以被当作包使用
        settings.py: 是项目的整体配置文件
        urls.py: 是项目的URL配置文件。可看作是你的django网站的目录
        wsgi.py：是web服务器和django框架交互的入口

    3.3创建应用（应用名：booktest）
        python manage.py startapp booktest

        应用目录说明：
        admin.py: 后台页面设置文件
        migrations: 数据迁移文件夹
        models.py: 写和数据库相关的内容，对应MVT中的--M
        views.py: 接收请求，进行处理，和M,T进行交互，返回应答，对应MVT中的--V
        tests.py: 用于软件测试用，暂不使用

        注意：此处需要将应用（booktest）添加至setting.py的INSTALLED_APPS配置中

    3.4开发服务器
        django提供了一个纯python编写的轻量级web服务器，仅在开发阶段使用
        python manage.py runsever 

        启动后，在浏览器运行：http：//127.0.0.1:8000/

        ctrl + c 停止服务器

4. 设计模型
    使用django进行数据库开发的步骤如下：
        4.1 在models.py中定义模型类
            from django.db import models

            class BookInfo(models.Model):
                btitle = models.CharField(max_length=20)
                bpub_date = models.DateField()
                def __str__(self):
                    return "%d" % self.id

            class HeroInfo(models.Model):
                hname = models.CharField(max_length=20)
                hgender = models.BooleanField()
                hcontent = models.CharField(max_length=100)
                hbook = models.ForeignKey(BookInfo)
                def __str__(self):
                    return "%d" % self.id
        
        4.2 迁移
            数据迁移的目的：django通过设计的模型类，自动生成数据表，django默认采用sqlite3数据库

            4.2.1 生成迁移文件：根据模型类生成创建表的语句
            命令：
                python manage.py makemigrations

            4.2.2 执行迁移：根据第一步生成的语句在数据库中创建表
            命令：
                python manage.py migrate

            注意：此处请确保应用（booktest）已添加至setting.py的INSTALLED_APPS配置中，否则会无法迁移

        4.3 在数据库中查看数据
            迁移完成后，项目根目录下会生成一个：db.sqlite3 文件
            在数据库图像界面打开此文件，即可看到数据表结构

5. 操作数据
操作数据的两种方式：
    5.1 通过shell命令行操作数据：python manage.py shell
        5.1.1添加数据
            >>> from booktest.models import BookInfo,HeroInfo
            >>> from datetime import date
            <!-- 添加书籍1 -->
            >>> b=BookInfo()
            >>> b.btitle="天龙八部"
            >>> b.bpub_date=date(1982,5,6)
            >>> b.save()
            <!-- 添加英雄1 -->
            >>> h=HeroInfo()
            >>> h.hname='乔峰'
            >>> h.hgender=False
            >>> h.hconten='降龙十八掌'
            >>> h.hbook=b
            >>> h.save()
            <!-- 添加书籍2 -->
            >>> b2=BookInfo()
            >>> b2.btitle="射雕英雄传"
            >>> b2.bpub_date=date(1990,3,4)
            >>> b2.save()
            <!-- 添加英雄2 -->
            >>> h2 = HeroInfo()
            >>> h2.hname = '郭靖'
            >>> h2.hgender = False
            >>> h2.hcontent = '降龙十八掌'
            >>> h2.hbook = b2
            >>> h2.save()
            <!-- 添加英雄3 -->
            >>> h3 = HeroInfo()
            >>> h3.hname = '黄蓉'
            >>> h3.hgender = True
            >>> h3.hcontent = '降龙十八掌'
            >>> h3.hbook = b2
            >>> h3.save()

        5.1.2 修改数据 
            >>> b1.btitle="鹿鼎记"
            >>> b1.save()

        5.1.3 删除数据
            h.delete()
        
        5.1.4 查找数据
            books = BookInfo.objects.all() 查找多条数据
            book = BookInfo.objects.get(id=1) 查找一条数据  -->查出来的只是一个id
            
            <!-- 显示数据的具体值 -->
            book.btitle,book.bpub_date -->要查找的数据之间用逗号隔开

            关联查询：
                图书和英雄之间是一对多的关系，django中提供了关联的操作方式获得关联集合
                b2.heroinfo_set.all() -->"射雕英雄传"这本书关联的英雄

    5.2 通过后台表格和表单的界面操作数据
        步骤：
            5.2.1管理界面本地化（将显示的语言、时间等使用本地的习惯） 
                LANGUAGE_CODE = 'zh-Hans'
                TIME_ZONE = 'Asia/Shanghai'
                注意：此处的时区使用亚洲/上海时区
            5.2.2创建管理员
                python manage.py createsuperuser
                    username:默认使用当前用户名（kk）
                    Email address: 遵循邮箱格式即可(python@163.com)
                    password:XXX (123456)
                注：括号中的设置为我的本地设置

                启动服务器：python manag.py runserver
                浏览器中输入：http://127.0.0.1:8000/admin 即可访问
                
            3.注册模型类
                登录后台管理后，默认没有我们创建的应用中定义的模型类，需要在自己应用中的admin.py文件中注册，可以在后台管理中看到，并进行CRUD操作。
                打开booktest/admin.py文件，编写如下代码：
                    from django.contrib import adim
                    from models import BookInfo,HeroInfo

                    admin.site.register(BookInfo)
                    admin.site.register(HeroInfo)
            4.自定义管理页面
                打开booktest/admin.py文件，自定义类，继承自admin.ModelAdmin类，属性list_display表示要显示哪些属性
             
6. 视图及URL
    视图开发步骤：1.定义视图 2.配置URL
    6.1 定义视图：
        视图就是一个python函数，第一个参数是HttpRequest类型的对象request,包含了所有请求的信息，视图必须返回HttpResponse对象，包含返回给请求者的响应信息
    6.2 配置URL
        需要两步完成URLconf配置

        a.打开项目配置文件夹中的urls.py文件，为urlpatterns列表增加项如下：
        urlpatterns = [
            url(r'^admin/', include(admin.site.urls)),
            url(r'^', include('booktest.urls'))  # 增加的一项
        ]
        b.在应用下创建urls文件，定义代码如下：
            from django.conf.urls import url
            from booktest import views
            urlpatterns = [
                url(r'^index$', views.index)
            ]

7.定义模板
    创建模板：在应用的平级目录创建templates文件夹，在文件夹下创建和应用同名的子文件夹，然后在与应用同名的子文件夹中创建模板文件。
    templates-->booktest-->index.html

    配置模板路径：
        在项目的settings.py文件中设置TEMPLATES的DIRS的值
        'DIRS':[os.path.join(BASE_DIR,'templates')]

    定义模板
        在模板中输出变量或者输入代码的语法:
            {{变量名}} 在模板中写变量
            注意：变量名必须由英文字符开始(A-Z或a-z)并可以包含数字字符、下划线和小数点(小数点在这里有特别的用途)，变量是大小写敏感的

            {%代码段%} 在模板中写python代码

    视图调用模板
        可以使用render函数来调用模板，render包含三个参数：
        第一个参数为request对象
        第二个参数为模板文件路径
        第三个参数为字典，表示向模板中传递的数据






            




