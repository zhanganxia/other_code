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
    # 打开一个模板
    f = open(g_templates_root + path)
    content = f.read()
    f.close()

    #从数据库获取数据
    conn = connect(host="localhost",user="test",password="mysql",port=3306,database="stock_prj",charset="utf8")
    cur = conn.cursor()
    sql = "select * from info"
    cur.execute(sql)
    ret = cur.fetchall()
    content_html="""
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
        html += content_html %(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[1])
        print(item[1])

    cur.close()
    conn.close()        
    # 完成数据的替换
    content = re.sub(r"\{%content%\}",html,content)
    return content

@route(r"/center\.html")
def center(path,pattern=None):
    """个人中心"""
    "/index.py  --> /index.html"
    f = open(g_templates_root + path)
    content = f.read()
    f.close()

    #从数据库获取数据完成替换
    conn = connect(host="localhost",user="test",password="mysql",database="stock_prj",port=3306,charset="utf8")
    cur = conn.cursor()
    sql = "select i.code,i.short,i.chg,i.turnover,i.price,i.highs,f.note_info from info as i inner join focus as f on i.id = f.info_id"
    cur.execute(sql)
    ret = cur.fetchall()
    content_html = """
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
                </tr>"""    
    html = ""
    for item in ret:
        html += content_html %(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[0],item[0])

    # 完成数据的替换
    content = re.sub(r"\{%content%\}", html, content)
    return content

@route(r"/update/(\d{6})\.html")
def update(path,pattern=None):
    ret = re.match(pattern,path)
    code = ret.group(1)

    f = open(g_templates_root + "/update.html",encoding="utf-8")
    content = f.read()
    f.close()

    conn = connect(host="localhost",user="test",password="mysql",database="stock_prj",port=3306,charset="utf8")
    cur = conn.cursor()

    sql="select i.short,f.note_info from info as i inner join focus as f on i.id = f.info_id where i.code = %s "
    cur.execute(sql,[code])
    ret = cur.fetchone()

    cur.close()
    conn.close()

    short = ret[0]
    note_info = ret[1]

    content = re.sub(r"\{%code%\}",short,content)
    content = re.sub(r"{%note_info%}",note_info,content)
    return content

@route(r"/add/(\d{6})\.html")
def add(path,pattern=None):
    ret = re.match(pattern,path)
    code = ret.group(1)

    #判断focus中是否已经添加
    conn = connect(host="localhost",user="test",password="mysql",database="stock_prj",port=3306,charset="utf8")
    cur = conn.cursor()
    sql = "select f.info_id from info as i inner join focus as f on i.id = f.info_id where i.code = %s"
    cur.execute(sql,[code])
    ret = cur.fetchone()
    if ret:
        return "不能重复添加，请重新选择！"

    #未添加的添加进focus
    sql = "insert into focus (info_id) select i.id from info as i where i.code = %s"
    cur.execute(sql,[code])
    conn.commit()
    cur.close()
    conn.close()
    return "恭喜你，添加成功！ %s"%code

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
    # 将body信息通过返回值传递给服务器
    # 读取对应路径下的模板数据 将模板数据做为body 数据返回给服务器
    # if path == "/index.py":
    #     # 获取index.html这个模板
    #     index(path)
    # if path == "/center.py":
    #     center(path)
    # 如果键不存在返回 None
    # 字典为什么不是一个空字典呢
    for pattern,func in g_func_path_dict.items():
        ret = re.match(pattern,path)
        if ret:
            return func(path,pattern)
    else:
        return "sorry, not found,没有对应的路径"

# application
