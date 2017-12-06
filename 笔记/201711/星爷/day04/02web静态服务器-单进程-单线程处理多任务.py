import socket
import re
import sys
import time


class HTTPServer(object):

    def __init__(self, port):
        '''服务器的初始化设置'''
        self.tcp_server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.tcp_server_socket.bind(('', port))
        self.tcp_server_socket.listen(128)
        # 设置服务器socket为非阻塞状态
        self.tcp_server_socket.setblocking(False)
        self.socket_list = []
        print(self.tcp_server_socket)
        #<socket.socket fd=3, family=AddressFamily.AF_INET, type=2049, proto=0, laddr=('0.0.0.0', 8080)>

    def run(self):
        while True:
            try:
                web_socket, web_addr = self.tcp_server_socket.accept()
            except Exception as ret:
                print("无客户端连接!", ret)
            else:
                print("新的客户端连接:", web_socket)
                self.socket_list.append(web_socket)
                # 设置客户端socket为非阻塞状态
                # web_socket.setblocking(False)
                # 遍历列表 查看哪些套接字有收到数据
                for web_socket in self.socket_list:
                    try:
                        request = web_socket.recv(2048)

                    except Exception as result:
                        print("没有收到数据", result)
                    else:
                        if request:
                            print("接收到来自%s的请求信息%s:" % (web_socket, request))
                            self.handle_with_request(request,web_socket)
                        else:
                            print("客户端%s已关闭!" % web_addr)
                            web_socket.close()
                            self.socket_list.remove(web_socket)
            time.sleep(2)

    def handle_with_request(self,request,web_socket):
        #分析请求读取对应的文件
        request = request.decode('utf-8')
        request_lines = request.splitlines()
        for item in request_lines:
            print(item)
    # GET /favicon.ico HTTP/1.1
    # GET /a/b/c/11.html HTTP/1.1
    # GET / HTTP/1.1
        request_index_lines = request_lines[0]

        ret = re.match(r"([^/]*) ([^ ]*) ", request_index_lines)
        method = ret.group(1)
        print(method)
        path = ret.group(2)
        

        if path == "/":
        # filename = input("请输入你要显示的内容:")
        # path = "/%s"%filename
            path = "/index.html"
        try:
        # 打开文件
            file = open("./html/html" + path, 'rb')
        except Exception as ret:
        # 404 报错
            response_header = "HTTP/1.1 404 OK\r\n"
            response_header += "content-type:text/html; charset=utf-8\r\n"
            response_header += "\r\n"
            response_body = "您访问的页面不存在".encode()
        else:
            # 读取二进制的数据
            content = file.read()
            file.close()

            response_header = "HTTP/1.1 200 OK\r\n"
            response_header += "\r\n"
            response_body = content
        finally:
            response = response_header.encode() + response_body
            web_socket.send(response)
            # 断开连接
            web_socket.close()
    

def main():
    # 整体的逻辑控制
    if len(sys.argv) == 2:
        # 判断端口号的格式,是不是数字
        if sys.argv[1].isdigit():
            port = int(sys.argv[1])
        else:
            print("请输入正确的端口号!")
    else:
        print("参数不够,请在文件名后添加端口号参数")
        return
    print(sys.argv)

    # 1.创建httpserver对象
    server = HTTPServer(port)
    # 2.调用对象的方法来启动服务器
    server.run()

    # port = sys.argv[1]
    # if sys.argv[]


if __name__ == '__main__':
    main()
