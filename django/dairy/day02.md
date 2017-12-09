day02 模型
1. 项目准备
    1.1 创建项目
    django-admin startprojrct test2

    1.2 创建应用
    python manage.py startapp booktest

    1.3 在pycharm中设置项目依赖的python环境
        虚拟环境下which python，复制路径，设置项目依赖
        /home/python/.virtualenvs/py3_django/bin/python
    
    1.4 安装应用（setting.py中设置）
        INSTALLED_APPS=(
            ...
            'booktest'
        )

    1.5 本地化（setting.py中设置）
        LANGUAGE_CODE = 'zh_Hans'
        TIME_ZONE = 'Asi/Shanghai'

    1.6 模板路径
        在应用同级目录下，创建template模板文件夹，在setting.py中配置：
        TEMPLATES = [
            {
                'DIRS':[os.path.join(BASE_DIR,'templates')],
                ...
            }
        ]
    1.7 准备视图，在应用文件中的views.py编写内容：
        from django.http import HttpReaponse

        def index(request):
        return HttpReaponse('hello world!')

    1.8 项目中匹配URL（在项目设置包中的url.py）
        urlpatterns = [
            ...
            url(r'^',include('booktest.urls'))
        ]
    1.9 在应用中匹配url，在应用中创建urls.py
        from django.conf.urls import url
        from booktest import views

        urlpatterns = [
            url(r'^index$',views.index)
        ]
    1.10 开启服务器，测试项目
        在shell虚拟环境下输入：python manage.py runserver

2. ORM-对象关系映射
    对象-关系映射ORM系统一般以中间件的形式存在，主要实现程序对象到关系数据库数据的一个映射
    使用ORM的好处：
        a. 实现了数据模型与数据库的解耦，通过简单的配置就可以轻松更换数据库，而不需要修改代码
        b. 只需要面向对象编程，不需要面向数据库编写程序

3. 使用mysql
    3.1 安装django操作操作mysql的包(python3下安装pymysql)
        pip install pymysql

    3.2 项目中使用数据库
        使用mysql数据库，数据库需要自己创建，不需要创建表。数据库的名字和项目名字尽量保持一致

        3.2.1 在项目配置文件夹下的__init__.py中添加如下内容：
            import pymysql
            pymysql.install_as_mySQLdb()

            登录mysql数据库，创建数据库名称为test2
            create database test2 charset=utf8

        3.2.2 在settings.py文件中的database一项中设置：
            DATABASES = {
                'default':{
                    'ENDINE'：'django.db.backends.mysql', #引擎为mysql
                    'NAME':'test2', #设置数据库名称
                    'USER':'root', #设置登录用户名
                    'PASSWORD':'mysql', #设置登录密码
                    'HOST':'localhost', #设置数据库主机地址
                    'PORT': '3306', #设置端口，默认是3306
                }
            }
        3.2.3 执行迁移，会自动在mysql数据库中创建表
            a. python manage.py makemigrations -->生成迁移文件
            b. python manage.py migrate --执行迁移        

4. 定义模型类

    4.1 定义模型类属性：
        属性名称 = models.字段类型（选项）

    4.2 属性名命名规则：
        a. 遵循python命名规范
        b. 不能使用连续的下划线，因为在查询中会用到连续下划线
        c. 指定字段类型
        d. 主键ID对应的属性不用定义，django会自动创建自增长主键列
    
    4.3 字段类型
        AutoField：自动增长的intergerFild,通常不用指定，Django会自动创建

        BooleanFild: 布尔字段，值为true或False
        NullBooleanField: 字符串，参数max_length表示最大字符个数
        CharField: 字符串，参数max_length表示最大字符个数
        TextField: 大文本字段，一般超4000个字符时使用
        IntegerField: 整数
        DecimalField: 十进制浮点数，参数max_digits表示总位数，参数decimal_places表示小数位数
        FloatField: 浮点数
        DateField: 日期，参数auto_now表示自动保存最新的修改日期，默认值False,参数auto_now_add表示自动保存创建时的日期，默认值False,两个参数不能同时设置
        TimeField : 事件，参数同DateField
        DateTimeField: 日期和时间，参数同DateField
        FileField: 上传文件字段
        ImageField: 继承于FileField，对上传的内容进行校验，确保是有效的图片

        4.3.1 关系字段类型
            Foreignkey: 一对多，将字段定义在多的一端中
            ManyToManyField： 多对多，将字段定义在两端中
            OneToOneField： 一对一，将字段定义在任意一端中
        
        4.3.2 字段类型选项
            null : 如果为True,表示允许为空，默认值是False
            blank: 如果为True，则该字段允许为空白，默认值是False
            db_column：字段的名称，如果未指定，则使用属性的名称
            db_index：若值为True, 则在表中会为此字段创建索引，默认值是False
            default：默认值
            primary_key：若为True，则该字段会成为主键，默认是False，一般作为AutoField的选项
            unique：如果为True, 这个字段在表中必须有唯一值，默认值是False

        4.3.3 元选项 （重要）
            生成的数据表默认名称为：'应用名称_模型类名称'，通过在模型类中定义类Meta,可以自定义表的名字
            class BookInfo(models.Model):
                ...
                class Meta: #元信息类
                    db_table = 'bookinfo' #指定表的名称

5. 模型成员
    5.1 模型实例方法：
        __str__():在将对象转换成字符串时会被调用
        save():保存或者修改模型对象到数据表中
        delete(): 将模型对象从数据表中删除

    5.2 模型类属性objects
        objects叫做管理器，是Manager类型的对象，定义在from django.db import models中
        用于模型对象和数据库交互
        object类属性是默认自动生成的，但是可以自定义管理器对象
        自定义管理器对象后，Django不再生成默认管理器对象objects

6. 查询集
    查询接表示从数据库中获取的对象集合，在管理器上调用过滤器方法会返回查询集，查询集可以含有一个或多个过滤器，过滤器基于所给的参数限制查询的结果。

    查询的特性：
        1.惰性执行:创建查询集不会访问数据库，直到调用数据时，才会访问数据库，调用数据的情况包括迭代、序列化等

        2.缓存：查询集的结果被存下来之后，再次查询时会使用之前缓存的数据

    过滤器：
        返回列表的过滤器：
            all():返回所有数据
            filter():返回满足条件的数据
            exclude(): 返回满足条件之外的数据,相当于sql语句中where部分的not关键字
            order_by():排序

        返回单个查询结果的过滤器：
            get()：返回单个满足条件的对象
            count(): 返回当前查询的总条数
            aggregate():聚合
            exists():判断查询集中是否有数据，如果有则返回True,如果没有则返回False

7. 条件查询
    条件查询相当于sql语句中的where的功能，条件在filter()、exclude()、get()方法中定义。
    语法：属性 + 两个下划线 + 比较运算符，所以属性名不能包括多个下划线
        属性名称__比较运算符=值

    条件查询的例子：
        # 1.获取所有图书
        books1 = BookInfo.objects.all()
        books1 = BookInfo.objects.shuminghao(books1)
        # 2.查询所有未逻辑删除的数据
        books2 = BookInfo.objects.total()
        # 3.查询id==1的数据
        books3 = BookInfo.objects.filter(id__exact=1) #等价于filter(id=1)
        # 4.模糊查询书名包含'传'的数据
        books4 = BookInfo.objects.filter(btitle__contains='传')
        # 5.模糊查询书名以”湖“结尾的书名
        books5 = BookInfo.objects.filter(btitle__endswith='湖')
        # 6.查询备注不为空的图书数据
        books6 = BookInfo.objects.filter(bcontext__isnull=False)
        # 7.范围查询，查询图书编号为1，3的数据
        books7 = BookInfo.objects.filter(id__in=[1,3])
        # 8.查询图书编号大于3的数据
        books8 = BookInfo.objects.filter(id__gt=3)
        # 9.查询发布日期为1986年的图书
        books9 = BookInfo.objects.filter(bpub_date__year=1986)
        # 10.查询id!=3的图书信息
        books10 = BookInfo.objects.exclude(id=3)
        # 11.查询阅读量大于等于评论量的图书信息
        books11 = BookInfo.objects.filter(bread__gte=F('bcommet'))
        # 12.查询id大于3且阅读量大于30的图书信息
        books12 = BookInfo.objects.filter(Q(id__gt=3)&Q(bread__gt=30))
        # 13.查询所有图书从大到小排列
        books13 = BookInfo.objects.all().order_by('-id')
        # 14.把id大于1的图书信息按阅读量从大到小排序显示
        books14 = BookInfo.objects.filter(id__gt=1).order_by('-bread')
        # 15.查询所有图书阅读量的总和
        books15 = BookInfo.objects.aggregate(Sum('bread'))['bread__sum']
        # 16.查询图书，要求图书中英雄的描述包含'十'
        books16 = BookInfo.objects.filter(heroinfo__hcontent__contains='十')

    比较查询：
        gt、gte、lt、lte：大于、大于等于、小于、小于等于

    日期查询：
        year、month、day、week_day、hour、minute、second：对日期时间类型的属性进行运算
    F对象：
        用于表字段之间的比较，使用之前需要先导入这个模块 
        from django.db.models import F
        
    Q对象：
        用于查询时的逻辑条件。not and or,可以对Q对象进行&|~(与或非)操作，使用之前需要先导入这个模块
        from django.db.models import Q

    查询结果排序：order_by

    聚合查询：
        对查询结果进行聚合操作，聚合函数包括：Avg,Count,Max,Min.Sum,被定义在django.db.models中，使用前要先导入：

        from django.db.models import Sum,Count,Max,Min,Avg
    连表查询：
        实现类似sql语句中的join查询语法
        关联模型类名小写__属性名__运算符=值
    
