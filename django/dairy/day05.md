1. 静态文件处理
    1.1 配置静态文件访问路径
        在settings.py文件中定义静态文件路径
        新建static文件夹，和应用平级
        具体设置如下：
            STATICFILES_DIRS=[
                os.path.join(BASE_DIRS,'static')
            ]

    1.2 访问/配置静态路径的步骤
        a. 在项目路径下的setting.py文件中查找定义的静态文件的访问路径
        b. 创建模板
        c. 在项目根目录（和应用平级）下创建static目录，再创建img、css、js 目录，在目录中放置静态文件
        d. 创建视图
        e. 配置URL
        f. 启动服务器查看页面效果
    
2. 中间件
    Django中的中间件是一个轻量级、底层的插件系统,可以介入Django的请求和响应处理过程，修改Django的输入输出

    内置方法：
        1) 初始化:__init()__方法
           作用：用于确定是否启用当前中间件，服务器响应第一个请求的时候调用一次

        2) 处理请求前：process_request(request)
           作用:在每个请求上调用，返回None或HttpResponse对象

        3）处理视图前：proccss_view(request,view_func,*view_args,**view_kwargs)
          作用：在每个请求上调用，返回None或HttpResponse

        4) 处理模板响应前：def process_template_response(request,response):
         作用：在每个请求上调用，返回实现了render方法的响应对象

        5）处理响应后：process_response(request,response)
        作用：所有响应返回浏览器之前被调用，在每个请求上调用，返回HttpResponse对象

        6) 异常处理：process_exception(request,exception)
        作用：当视图抛出异常时调用，在每个请求上调用，返回一个HttpResponse对象
        
    自定义中间件配置：
        需在项目配置下的setting.py文件中，向MIDDLEWARE_CLASSES        

    在模板文件中引入静态文件
        使用反向解析定义资源文件地址，需要先定义下面的文件路径
    {% load static from staticfiles %}

3. Admin站点
    3.1 使用Admin站点功能
        1）创建超级管理员
        python manage.py createsuperuser

        2）注册模型类
        admin.site.register(<模型类>)

        3）通过用户名和密码登录后台界面

    3.2 控制管理页面展示
        应用中的admin.py中添加ModelAdmin可以控制模型在Admin界面中的展示方式，主要包括在列表页的展示方式、添加修改页的展示方式

        在注册模型类前定义管理类AreaAdmin：
        class AreaAdmin(admin.ModelAdmin)

        管理类的两种使用方式：
            a.注册参数
                admin.site.register(AreaInfo,AreaAdmin)

            b.装饰器
                @admin.register(AreaInfo)
                class AreaAdmin(admin.ModelAdmin):
                    pass

    3.3 管理页面的选项操作控制

        3.3.1 列表页选项
            1）页大小（每页显示多少条数据）
                list_per_page=100
            
            2）操作选项的设置(设置操作选项显示位置)
                action_on_top = True/False
                action_on_bottom = True/False

            3) 列表中显示的列
                list_display=[模型字段1，模型字段2，...]

                点击列头可以进行升序或者降序排列

            4) 将方法作为列
                列可以是模型字段,还可以是模型方法,要求方法有返回值
                例:
                修改模型类
                class AreaInfo(model.Model):
                    ...
                    def title(self):
                        return self.atitle

                修改AresAdmin类
                class AreaAdmin(admin.ModelAdmin):
                    ...
                    list_display = ['id','atitle','title']

                注意:方法列是不能进行排序的,如果要排序需要为方法指定排序的依据
                admin_order_field = 模型类字段

            5) 列标题
                列标题默认为属性或方法的名称,可以通过属性设置,需要先将模型字段封装成方法,再对方法使用这个属性,模型字段不能直接使用这个属性

                short_description='列标题'

            6) 关联对象
                无法直接访问关联对象的属性或方法,可以在模型类中封装方法,访问关联对象的成员
                例如：
                修改模型类：
                class AreaInfo(models.Mode):
                    ...
                    def parent(self):
                        return self.aParent.atitle
                parent.short_description='父级区域名称'

                修改AreaAdmin类
                    class AreaAdmin(admin.ModelAdmin):
                        ...
                        list_display = ['id','atitle','title','parent']

            7) 右侧过滤器
                list_filter=['字段名']

            8）搜索栏
                search_fields = ['字段名']

            9）中文标题
                修改模型类，为属性指定verbose_name参数，即第一个参数
                class AreaInfo(models.Model):
                atitle = models.CharField('标题'，max_length=30)

        3.2.2 编辑页选项
            
            1）显示字段顺序：field=['字段1','字段2']，写的顺序不一样，最终的排列顺序页不一样

            2）分组显示
            fieldset=(
                ('组1标题'，{'fields':('字段1','字段2')}),
                ('组2标题'，{'fields':('字段3'，'字段4')})
            )

            说明：fields与fieldsets两者选一使用

            3）关联对象
                在一对多的关系中，可以在一端的编辑页面中编辑多端的对象，嵌入多端对象的方式包括表格、块两种：
                inlineModelAdmin:表示在模型的编辑页面嵌入关系模型的编辑；
                
                子类TabularInline：以表格的形式嵌入
                子类StackedInline: 以块的形式嵌入
             
        3.2.3 重写模板
            步骤：
            1.在template/目录下创建admin目录
            2.在当前虚拟环境中Django的目录，再向下找admin模板
                /home/python/.virtualenvs/py_django/lib/python3.5/site-packages/django/contrib/admin/templates/admin
            3. 


    4.上传图片
        form表单属性必须添加：enctype="multipart/form-date"

        chunks() 方法可以将图片图书进行分块