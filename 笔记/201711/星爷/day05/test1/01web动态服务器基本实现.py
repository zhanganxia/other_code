import socket
import sys
import re
import time
import gevent
from gevent import monkey

monkey.patch_all()

class HTTPServer(object):

    def __init__(self,port):
        '''服务器的初始化设置'''
        self.tcp_server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.tcp_server_socket.bind(('', port))
        self.tcp_server_socket.listen(128)
        #self.tcp_server_socket.setblocking(False)
        #self.socket_list = []

        print(self.tcp_server_socket)

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
            response_head = "HTTP/1.1 200 OK\r\n"
            response_head += "content-type:text/html; charset=utf-8\r\n"
            data_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            #需要获取字节长度
            response_head += "content-length:%d\r\n" % len(data_time)
            
            response_head += "\r\n"
            #response_body = content

            response = response_head + data_time
            web_socket.send(response.encode())
            # 断开连接
            #web_socket.close()


def main():
    if len(sys.argv) == 2:
        #判断端口号的格式是不是数字
        if sys.argv[1].isdigit():
            port = int(sys.argv[1])
        else:
            print("请输入正确的端口号!")
    else:
        print("参数不够,请在文件名后添加端口号参数")
        return
    print(sys.argv)

    server = HTTPServer(port)
    server.run()


if __name__ == '__main__':
    main()
