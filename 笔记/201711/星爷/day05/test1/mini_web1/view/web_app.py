import time

def app(environ, start_response):
    '''
    :param environ: 服务器传递的参数 是字典类型
    :param start_reaponse:服务器模块中函数的引用
    :return :返回body信息
    '''
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html')]
    start_response(status,response_headers)
    return str(environ) + '==Hello world from a simple WSGI application! --->%s\n'% time.ctime()