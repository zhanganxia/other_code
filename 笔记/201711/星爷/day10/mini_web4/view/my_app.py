import time
import re
from pymysql import *

g_templates_root = "./templates"
g_func_path_dict = {}


# 让文件路径和被装饰的函数一一对应
# 一个路径对应这个一个可以执行获取数据的函数  --> 路由
def route(path):
    print("++++++函数已经被执行了+++++++")
    def warpper(func):
        # 装饰器完成对应的关键部分:装饰函数 将文件路径作为key 将函数引用作为value 存储到字典中
        g_func_path_dict[path] = func
        def inner():
            # 此段代码根本没有执行到
            func()
        return inner
    return warpper


# 可以通过带有参数的装饰器来完善代码
# 1. 调用了route("/index.py")  --> warpper
# 2. 将route函数执行的返回值当做装饰器函数开始装饰 index = warpper(index)
@route(r"/index\.html") # 在装饰器中将 index方法 和 xxx 完成一个映射关系(一对一的关系)
def index(path,pattern=None):

    """首页"""
    # 打开一个模板文件
    #path = path.replace(".py", ".html")
    f = open(g_templates_root + path)
    content = f.read()
    f.close()
    conn = connect(host="localhost",
                        user = "test",
                        password = "mysql",
                        database = "stock_prj",
                        port = 3306,
                        charset = "utf8")
    cur = conn.cursor()
    sql = "select * from info"
    cur.execute(sql)
    ret = cur.fetchall()

    templet_html = """
            <tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>
                    <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="%s">
                </td>                
            </tr>
             """
    html = ""
    for item in ret:
        html += templet_html % (item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[1])
        print(item[1],"**********")
    # 在模板添加动态数据
    #html = "<h1>首页数据: 这里是从mysql数据库中读取的动态数据</h1>"
    cur.close()
    conn.close()
    # 完成数据的替换
    content = re.sub(r"\{%content%\}",html,content)
    return content

#index("/index.py")

@route(r"/center\.html")
def center(path,pattern=None):
    """个人中心"""

    #path = path.replace(".py", ".html")
    "/index.py  --> /index.html"
    f = open(g_templates_root + path)
    content = f.read()
    f.close()
    conn = connect(host="localhost",
                        user = "test",
                        password = "mysql",
                        database = "stock_prj",
                        port = 3306,
                        charset = "utf8")
    cur = conn.cursor()
    sql = "select i.code,i.short,i.chg,i.turnover,i.price,i.highs,f.note_info from info as i inner join focus as f on i.id = f.info_id"
    cur.execute(sql)
    ret = cur.fetchall()
    template_html = """
                <tr>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>
                        <a type="button" class="btn btn-default btn-xs" href="/update/%s.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
                    </td>
                    <td>
                        <input type="button" value="删除" id="toDel" name="toDel" systemidvaule=%s>
                    </td>
                </tr>
    """
    html = ""
    for item in ret:
        html += template_html % (item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[0],item[0])   
    #html = "<h1>个人中心数据: 这里是从mysql数据库中读取的动态数据</h1>"
    # 完成数据的替换
    content = re.sub(r"\{%content%\}", html, content)
    return content

@route(r"/update/(\d{6})\.html")
def update(path,pattern=None):
    #根据正则表达式在path路径中提取股票的code码
    ret = re.match(pattern,path)
    code = ret.group(1)
    #打开模板
    f = open(g_templates_root + "/update.html",encoding="utf-8")
    content = f.read()
    f.close()

    conn = connect(host="localhost",
                        user = "test",
                        password = "mysql",
                        database = "stock_prj",
                        port = 3306,
                        charset = "utf8")
    cur = conn.cursor()
    #根据code码获取股票的名字和描述信息
    sql = "select i.short,f.note_info from info as i inner join focus as f on i.id = f.info_id where i.code = %s"
    cur.execute(sql,[code])
    ret = cur.fetchone()

    cur.close()
    conn.close()

    #获取名字和描述信息
    short = ret[0]
    note_info = ret[1]

    #根据code码获取股票的名字和描述信息
    content = re.sub(r"\{%code%\}",short, content)
    content = re.sub(r"{%note_info%}",note_info, content)
    #完成数据的替换
    #返回数据
    return content

@route(r"/add/(\d{6})\.html")
def add(path, pattern=None):
    #根据正则表达式，在path路径中提起code码
    ret = re.match(pattern, path)
    code = ret.group(1)
    print(code,"--------------------------")

    #向focus表中插入数据
    conn = connect(host="localhost",
                        user = "test",
                        password = "mysql",
                        database = "stock_prj",
                        port = 3306,
                        charset = "utf8")
    cur = conn.cursor()
    #已知code获取对应的id
    #insert select

    #判断是否已经被关注
    sql = "select * from focus where info_id = (select id from info where code = %s)"
    cur.execute(sql, [code])
    ret = cur.fetchone()
    if ret:
        return "已经关注了该股票,请不要重复关注"

    sql = "insert into focus (info_id) select id from info where code = %s"
    cur.execute(sql, [code])

    conn.commit()
    cur.close()
    conn.close()

    return "关注股票成功！%s" % code

def app(environ, start_response):
    """
    :param environ: 服务器传递的参数  是字典类型
    :param start_response: 服务器模块中的函数的引用
    :return: 返回body信息
    """
    path = environ["PATH_INFO"]
    print(path, "在框架中被打印++++")
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html')]
    # 响应头信息传递给服务器
    start_response(status, response_headers)
    #实际的使用是根据一个路径获取一个方法的引用
    #{正则表达式：方法引用}
    #path = "/center.html"
    #{r"/center}
    #获取正则表达式，根据正则表达式到path中提取信息
    #如果能够提取到就认为是一一对应，否则就不是一一对应

    #pattern是正则路径
    #func是函数
    for pattern,func in g_func_path_dict.items():
        ret = re.match(pattern,path)
        print("$$$$$",pattern)
        if ret:
            #正则表达式和path是匹配的
            return func(path, pattern)
    else:
        #字典中正则表达式都遍历完了，也没有能够和path匹配
        return "sorry, not found,没有对应的路径"

# application
