参考地址：http://djangobook.py3k.cn

django.contrib包
    管理工具：djando.contrib.admin
    Django自动化管理工具是django.contrib的一部分。
    django.contrib是一套庞大的功能集，它是Django的基本代码的组成部分    


URLconf
    ---------------------------------------
    from django.conf.urls.defaults import * -->Django URLconf的基本构造，包含一个patterns函数

    urlpatterns = patterns('',)  -->pattern函数中的空字符串可以被用来表示一个视图函数的通用前缀（当前目录）
    ---------------------------------------
    urlpatterns中传入新的路径('^hello$',hello) -->URLpattern,它是一个python元组，该元组中有两个元素：元素1--模式匹配正则；元素二--元素一匹配的模式将使用的视图函数
    
在虚拟环境中启动python交互界面为什么用python manage.py shell而不是python？
    这两个命令都会启动交互解释器，但是manage.py shell命令有一个重要的不同：在启动解释器之前，它告诉Django使用哪个设置文件。Django框架的大部分子系统，包括模板系统，都依赖与配置文件；如果django不知道使用哪个配置文件，这些系统将不能工作

    Django搜索DJANGO_SETTINGS_MODULE环境变量，它被设置在settings.py中，在运行命令：python manage.py shell，它将自动处理：DJANGO_SETTINGS_MODULE

创建一个Template对象，模板做了哪些事情？
    创建一个Template对象的时候，模板系统在内部便宜这个模板到内部格式，并做优化，做好渲染的准备。如果模板语法有错误，在调用Template()时就会抛出TemplateSyntaxError异常

引发TemplateSyntaxError异常的情形？
    1.无效(Invalid)的tags
    2.标签的参数无效
    3.无效的过滤器
    4.过滤器的参数无效
    5.无效的模板语法
    6.未封闭的块标签(针对需要封闭的块标签)

如何进行模板渲染？
    一旦创建一个Template对象，可以用context来传递数据给它。一个context是一系列变量和它们值的集合。
    context在Django里表现为Context类，在django.template模块里。它的构造函数带有一个可选的参数：一个字典映射变量和它们的值。调用Template对象的render()方法并传递context来填充模板。

    使用Django模板系统的基本规则:写模板，创建Tempate对象，创建context，调用render()方法

在框架中，Django会一直使用Unicode对象而不是普通的python字符串，可以通过字符串前的u来区分。范例：下文中 t.render(c)返回的值是一个Unicode对象：
    >>> from django.template import Context, Template
    >>> t = Template('My name is {{ name }}.')
    >>> c = Context({'name': 'Stephane'})
    >>> t.render(c)
    u'My name is Stephane.'

字典和contexts的区别？
    python的字典数据类型就是关键字和它们的值的一个映射。
    Context和字典很类似，Context还提供更多的功能

Django深度变量的查找
    在Django模板中遍历复杂数据结果的关键是句点字符(.)
    当模板系统在变量名中遇到点时，按照以下顺序尝试进行查找：
        1.字典类型查找（比如foo['bar']）
        2.属性查找（比如foo.bar）
        3.方法调用（比如foo.bar）
        4.列表索引查找（比如foo[bar]）
    系统使用找到的第一个有效类型。这是一种短路逻辑

    使用句点(dot)查找--dot lookup的访问函数功能时，需要注意的问题：
        1.当在模板代码中执行的函数抛出异常时，会一直向上传播，除非这个异常中有一个参数：silent_variable_failure=True;这样的话，这个出错信息就会被渲染成空字符串。
        >>> class SilentAssertionError1(AssertionError):
        ...     silent_variable_failure = True
        ... 
        >>> class PersonClass5:
        ...     def first_name(self):
        ...       raise SilentAssertionError1()
        ... 
        >>> p1 = PersonClass5()
        >>> t.render(Context({"person":p1}))
        'My name is '
        >>> 

        2.很明显，调用函数会产生一些不好的结果，安全漏洞之类的，如果你有一个BankAccout，
        然后在模板中写成{{account.delete}}这样的标签，其中"account"又是BankAccount的一个实例，请注意在这个模板载入时，account对象将被删除。
        要防止这样的事情发生，必须设置该方法的alters_data函数属性：
        def delete(self):
            #Delete the account
            delete.alters_data=True

        模板系统不会执行任何以该方式进行标记的方法，接上面的例子，如果模板文件里包含了{{ account.delete }},对象又具有delete()方法，而且delete()方法有alters_data=True这个属性，那么在模板载入时，delete()方法将不会被执行。它将静静地错误退出
    
    如何处理无效变量
        默认情况下，如果一个变量不存在，模板系统会把它展示为空字符串，不做任何事情来表示失败。

基本的模板标签和过滤器
    1.标签 if/else
        {% if %}标签检查(evaluate)一个变量，如果这个变量为真(即，变量存在，非空，不是布尔值假)，系统会显示在{% if %}和{% endif %}之间的任何内容，例如：
        {% if today_is_weekend %}
            <p>Welcome to the weekend!</p>
        {% endif %}
        {% else %}标签是可选的

    在Python和Django模板系统中，以下这些对象相当于布尔值的False
        空列表([])、空元组(())、空字典({})、空字符串('')、零值(0)、特殊对象None、对象False(很明显)
    
        使用规则
            1.1 {% if %}标签接受and,or或者not关键字来对多个变量做判断，或者对变量取反not

            1.2 {% if %}标签不允许在同一个标签中同时使用and和or,逻辑可能模糊
                例：{% if a_list and b_list or c_list %}

            1.3 模板不支持用圆括号来组合比较操作。如果需要组合表达逻辑，有两种方法：
                a. 在模板之外用圆括号(),组合表达逻辑式，以模板变量的形式传给模板
                b. 用嵌套的{% if %}标签替换
                    {% if a_list %}
                        {% if b_list and c_list %}
                            ...
                        {% endif %}
                    {% endif %}

            1.4 允许多次使用同一个逻辑操作符，不允许组合使用不同的逻辑操作符
                {% if a_list or b_list or c_list %}
    2.标签for循环
        在每个{% for %}循环里有一个称为"forloop"的模板变量。这个变量有一些提示循环进度信息的属性。
        forloop.counter总是一个表示当前循环的执行次数的整数计数器。这个计数器是从1开始的，所以在第一次循环时forloop.counter将会被设置为1












