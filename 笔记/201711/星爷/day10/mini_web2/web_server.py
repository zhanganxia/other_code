# from socket import *  # 不能够使用这种方式导入对象 就会导致monkey给socket模块打补丁失败
import socket
import re
import sys
import gevent
from gevent import monkey


monkey.patch_all()

g_view_root = "./view"
g_static_root = "./static"



class HTTPServer(object):

    def __init__(self, port, app):
        """服务器的初始化设置"""
        # 1. 创建服务器的socket 做服务器初始化的设置
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.server_socket)  # gevent._socket3.socket
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 2. 绑定信息
        self.server_socket.bind(("", port))
        # 3. 变为被动的套接字
        self.server_socket.listen(128)
        self.app = app
        self.resp_headers = None

    def run(self):
        """运行服务器"""
        # 4. 等待新的客户端连接
        while True:
            # 一旦有客户端连接 就创建进程为该顾客服务
            new_socket, new_addr = self.server_socket.accept()
            # 创建子进程 线程共享进程资源 不会发生资源的拷贝
            # join 等待所有的协程任务执行完毕 产生一种阻塞
            # 此时不需要join 因为在while True 死循环里面
            gevent.spawn(self.handle_with_request, new_socket)

    def handle_with_request(self, new_socket):
        # 接收数据
        while True:
            req = new_socket.recv(2048)
            # 如果接收的数据位空 关闭连接即可
            if not req:
                # close()
                new_socket.close()
                # 退出当次循环  协程任务也会推出
                return
            # 6. 分析请求 读取对应的文件 将文件数据发送给浏览器
            # print(req.decode())
            req = req.decode()
            req_lines = req.splitlines()
            for item in req_lines:
                # 验证 请求头信息中最后一行是空行
                print(item)
            # 获取第一行
            req_line = req_lines[0]
            # GET /favicon.ico HTTP/1.1
            # GET /a/b/c/11.html HTTP/1.1
            # GET / HTTP/1.1
            # 正则表达式
            # ret = re.match(r"(.*) (.*) ", req_line)
            # [^a-z] 不能够以 / 开头
            ret = re.match(r"([^/]*) ([^ ]*)", req_line)
            method = ret.group(1)
            print(method)
            path = ret.group(2)
            print(path)
            # 区分动态和静态
            if path == "/":
                    # 当用户直接在浏览器中输入127.0.0.1:8080 或者localhost:8080  --> GET / HTTP/1.1 --> /
                    path = "/index.html"
            if path.endswith(".html"):
                # 动态的网页数据
                print("动态数据")
                environ = {
                    "PATH_INFO":path
                }
                response_body = self.app(environ, self.start_response)
                # 获取状态信息
                resp_header = self.resp_headers[0]
                # 获取响应行信息
                resp_lines = self.resp_headers[1]
                resp_header = "HTTP/1.1 %s\r\n" % resp_header
                for key, value in resp_lines:
                    resp_header += "%s:%s\r\n" % (key, value)
                # 缺少了空行 和长度(长连接)
                # 添加长度
                resp_header += "content-length:%d\r\n" % len(response_body.encode())
                resp_header += "\r\n"
                resp = resp_header + response_body
                new_socket.send(resp.encode())
            else:
                # ./static/css/bootstrap.min.css
                # 静态(.html, .png, .js .css)
                
                resp = ""
                try:
                    # 需要将".html" 修改为静态资源对应的路径
                    f = open(g_static_root + path, "rb")
                except Exception as ret:
                    # 404错误
                    response_body = "sorry, 您访问的页面不存在".encode()
                    response_header = "HTTP/1.1 404 Not Found\r\n"
                    # response_header += "content-type:text/html; charset=utf-8\r\n"
                    response_header += "content-length:%d\r\n" % len(response_body)
                    response_header += "\r\n"
                else:
                    # 打开文件成功
                    # 读取二进制的数据
                    content = f.read()
                    f.close()
                    response_header = "HTTP/1.1 200 OK\r\n"
                    # 解决编码的问题 如果指定文件类型 就会导致.css 和 .js文件接收失败
                    # response_header += "content-type:text/html; charset=utf-8\r\n"
                    # 需要获取字节长度
                    response_header += "content-length:%d\r\n" % len(content)
                    response_header += "\r\n"
                    response_body = content
                finally:
                    resp = response_header.encode() + response_body
                    new_socket.send(resp)
                    # 7. 断开连接 new_socket 服务端套接字先close 浏览器就能够知道数据已经接受完毕
                    # new_socket.close()

    def start_response(self, status, response_headers):
        self.resp_headers = [status, response_headers]

def main():
    # 以后通过 python3 xx.py 8888 my_app:app 来运行服务器
    # 一定是这种分支结构更好
    print(sys.path)
    sys.path.insert(0, g_view_root)
    print(sys.path)
    if len(sys.argv) != 3:
        # 不是两个参数 先处理错误的情况
        print("请以 python3 xx.py 8888 my_app:app 来运行服务器")
        return
    if not sys.argv[1].isdigit():
        print("请输入正确的端口号")
        return
    # 一定是正确主逻辑
    port = int(sys.argv[1])
    # 提取第三个参数
    moudle_method_params = sys.argv[2]
    # 通过冒号切割
    parmas = moudle_method_params.split(":")
    print(parmas)
    moudle_name = parmas[0]
    method_name = parmas[1]
    # 通过模块名动态导入对应的模块 使用 __import__ 内建函数
    # 作业通过动态导入的方式获取另外一个模块的类 --> 通过动态获取的类创建对象并且调用对象方法
    app_moudle = __import__(moudle_name)
    # 在对应的模块中获取对应的函数
    app_method = getattr(app_moudle,method_name)
    print(app_moudle, app_method)


    # 整体的逻辑控制
    # 1. 创建HTTPServer对象
    server = HTTPServer(port, app_method)
    # 2. 调用对象的对象方法来启动服务器
    server.run()


if __name__ == '__main__':
    main()
