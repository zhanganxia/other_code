import socket
import sys
import re
import time
import gevent
from gevent import monkey

monkey.patch_all()

g_view_root = "./view"
g_static_root = "./static"

class HTTPServer(object):

    def __init__(self,port,app):
        '''服务器的初始化设置'''
        self.tcp_server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.tcp_server_socket.bind(('', port))
        self.tcp_server_socket.listen(128)
        #self.tcp_server_socket.setblocking(False)
        #self.socket_list = []

        #print(self.tcp_server_socket)
        self.app = app
        #跨函数调用
        self.resp_headers = None

    def run(self):
        while True:
            #等待对方链接
            web_socket, web_addr = self.tcp_server_socket.accept()
            #创建子进程  线程共享进程资源 不会发生资源的拷贝
            gevent.spawn(self.handle_with_request,web_socket)
    def handle_with_request(self, web_socket):
        #为这个浏览器服务
        while True:
            request = web_socket.recv(2048)
           #如果接收的数据为空关闭连接即可
            if not request:
                web_socket.close()
                #退出当前循环,协程任务也会退出
                return
            req = request.decode()
            request_lines = req.splitlines()
            # for item in request_lines:
            #     print(item)
            req_line = request_lines[0]
            # print(req_line)
            uri = req_line.split(" ")
            # ['GET', '/index.py', 'HTTP/1.1']
            # ret = re.match(r"([^/]*) ([^]*)",req_line)
            print("*****************")
            method = uri[0]
            print(method)
            path = uri[1]
            print(path)

            #伪静态-->动态url地址，以html结尾
            if path == "/":
                    path = "/index.html"
            print(path, "+++++++++++++++++++++++++")
            #区分动态和静态
            if path.endswith(".html"):
                #动态的网页数据
                print("动态数据")
                environ = {
                    "PATH_INFO":path
                }
                response_body = self.app(environ,self.start_response)
                #获取状态信息
                response_header = self.resp_headers[0]
                #获取响应行信息
                response_lines = self.resp_headers[1]
                print("#######################")
                print(response_lines)

                #拼接请求头信息
                response_header = "HTTP/1.1 %s \r\n"%response_header

                for key, value in response_lines:
                    response_header += "%s:%s\r\n"%(key,value)
                #缺少了空行和长度(长连接)
                #添加长度
                response_header += "content-length:%d\r\n" % len(response_body.encode())
                response_header += "\r\n"

                resp = response_header + response_body
                web_socket.send(resp.encode())
            else:
                #res = ""
                print("ccc33")
                try:
                    f = open(g_static_root + path,"rb")
                except Exception as ret:
                     # 404错误
                    content = u"sorr,您访问的页面不存在不输入打字输入法".encode("utf-8")
                    response_header = "HTTP/1.1 404 Not Found\r\n"
                    response_header += "content-type:text/html; charset=utf-8\r\n"
                    response_header += "content-length:%d\r\n" % len(content)
                    response_header += "\r\n"
                else:
                    content = f.read()
                    f.close()
                    response_header = "HTTP/1.1 200 OK\r\n"
                    response_header += "content-length:%d\r\n" % len(content)
                    
                    response_header += "\r\n"
                    #response_body = content

                response = response_header.encode("utf-8") + content
                print(response)
                web_socket.send(response)
                    # 断开连接
                # web_socket.close()

    def start_response(self,status,response_headers):
        self.resp_headers = [status,response_headers]


def main():
    
    sys.path.insert(0, g_view_root)
    print(sys.path)
    
    #一定是这种分支结构
    #逆向思维,先处理错误的情况
    if len(sys.argv) != 3:
        #不是两个参数 先处理错误
        print("请输入完整参数:python3 文件名 端口号 模块名:方法名")
        return
    if not sys.argv[1].isdigit():
        print("请输入正确的端口号!")
        return
    #一定是正确的逻辑
    #端口号
    port = int(sys.argv[1])
    my_app = sys.argv[2].split(":")
    #此处的my_app是列表类型的
    print("###############",my_app)
    model_name = my_app[0]
    method_name = my_app[1]
    #导入web框架的主模块
    web_fram_module = __import__(model_name)
    #获取那个可直接调用的函数
    app = getattr(web_fram_module,method_name)

    print("-------------",model_name,method_name)
    server = HTTPServer(port,app)
    server.run()


if __name__ == '__main__':
    main()
