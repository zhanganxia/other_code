import socket
import gevent
import re
import sys
from gevent import monkey

monkey.patch_all()

g_view_root = "./view"
g_static_root = "./static"

class HTTPServer(object):
    def __init__(self,port,app):
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
        self.server_socket.bind(('',port))
        self.server_socket.listen(128)
        #self.server_socket.setblocking(False)
        self.app = app
        self.resp_headers = None
    def run(self):
        while True:
            new_socket,new_addr = self.server_socket.accept()
            gevent.spawn(self.handle_with_request,new_socket)
    def handle_with_request(self,new_socket):
        while True:
            req = new_socket.recv(2048)
            if not req:
                new_socket.close()
                return
            req.decode("utf-8")
            req_lines = req.splitlines()
            req_line = req_lines[0]

            ret = re.match(r"([^/]*) ([^ ]*)",req_line)
            method = ret.group(1)
            path = ret.group(2)

            if path.endswith(".py"):
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
                if path == "/":
                    # 当用户直接在浏览器中输入127.0.0.1:8080 或者localhost:8080  --> GET / HTTP/1.1 --> /
                    path = "/index.html"
                # 打开文件 打开一个不存在的文件 No such file or directory: './html/a/c/b.html'
                # 提高程序的健壮性
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

        
    def start_response(self,status,response_header):
        self.resp_headers = [status,response_header]


def main():
    sys.path.insert(0,g_view_root)
    if len(sys.argv) != 3:
        print("请以 python3 xx.py 8888 来运行服务器")
        return
    if not sys.argv[1].isdigit():
        print("请输入正确的端口号")
        return
    port = int(sys.argv[1])
    module_method_params = sys.argv[2]
    parmas = module_method_params.split(":")
    moudle_name = parmas[0]
    method_name = parmas[1]
    
    app_moudle = __import__(moudle_name)
    app_method = getattr(app_moudle,method_name)

    server = HTTPServer(port,app_method)
    server.run()

if __name__ == '__main__':
    main()
    