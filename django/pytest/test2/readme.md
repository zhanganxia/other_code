day02 模型
创建数据库（数据库名尽量和项目名一致）
2.使用mysql
    2.1 安装django操作操作mysql的包(python3下安装pymysql)
        pip install pymysql

3.定义模型类
    3.1 定义模型类属性：
    属性名称 = models.字段类型（选项）

    3.2 属性名命名规则：
        a. 遵循python命名规范
        b. 不能使用连续的下划线，因为在查询中会用到连续下划线
        c. 指定字段类型
        d. 主键ID对应的属性不用定义，交给Django来做