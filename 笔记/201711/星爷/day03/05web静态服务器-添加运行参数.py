import socket
import re
import sys

class HTTPServer(object):
    def __init__(self,port):
        '''服务器的初始化设置'''
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.tcp_server_socket.bind(('', port))
        self.tcp_server_socket.listen(128)
    def run(self):
        while True:
            web_socket, web_addr = self.tcp_server_socket.accept()
            request = web_socket.recv(2048)
            #如果接收的数据位空,关闭连接即可
            if not request:
                #close()
                web_socket.close()
                #退出当次循环
                continue
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
            #404 报错
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
    #整体的逻辑控制
    if len(sys.argv) == 2:
        #判断端口号的格式,是不是数字
        if sys.argv[1].isdigit():
            port = int(sys.argv[1])
        else:
            print("请输入正确的端口号!")
    else:
        print("参数不够,请在文件名后添加端口号参数")
        return
    print(sys.argv)

    #1.创建httpserver对象
    server = HTTPServer(port)
    #2.调用对象的方法来启动服务器
    server.run()

    # port = sys.argv[1]
    # if sys.argv[]


if __name__ == '__main__':
    main()
