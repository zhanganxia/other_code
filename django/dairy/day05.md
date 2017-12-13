静态文件处理
    1.在settings.py文件中定义静态文件路径
    新建static文件夹，和应用平级
    具体设置如下：
        STATICFILES_DIRS=[
            os.path.join(BASE_DIRS,'static')
        ]

    2.在模板文件中引入静态文件
        使用反向解析定义资源文件地址，需要先定义下面的文件路径
    {% load static from staticfiles %}

    3. 中间件

    4.上传图片
        form表单属性必须添加：enctype="multipart/form-date"

        chunks() 方法可以将图片图书进行分块