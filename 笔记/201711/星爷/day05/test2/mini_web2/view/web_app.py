import time
import re

g_templates_root = "./templates"

def index(path):
    '''首页'''
    path = path.replace(".py",".html")
    f = open(g_templates_root + path)
    content = f.read()
    f.close()

    html = "<h1>首页数据：这里是从mysql数据库中读取的动态数据</h1>"
    #完成数据的替换
    content = re.sub(r"\{%content%\}", html, content)
    return content

def center(path):
    '''个人中心'''
    path = path.replace(".py",".html")
    "/center.py --> /center.html"
    f = open(g_templates_root + path)
    content = f.read()
    f.close()
    html = "<h1>个人中心数据：这里是从mysql数据库中读取的动态数据</h1>"
    #完成数据的替换
    content = re.sub(r"\{%content%\}", html, content)

    return content

g_func_path_dict = {
    "/index.py" : index,
    "center.py" : center
}

def app(environ, start_response):
    '''
    :param environ: 服务器传递的参数 是字典类型
    :param start_reaponse:服务器模块中函数的引用
    :return :返回body信息
    '''
    path = environ["PATH_INFO"]
    print(path,"在框架中被打印+++")

    status = '200 OK'
    response_headers = [('Content-Type', 'text/html')]
    start_response(status,response_headers)
    func = g_func_path_dict.get(path)

    if func:
        #返回body的数据
        return func(path)
    else:
        return "没有对应的路径"

    #return str(environ) + '==Hello world from a simple WSGI application! --->%s\n'% time.ctime()