import socket
import re
import sys
#import multiprocessing
#import threading
import gevent
from gevent import monkey
#web静态页面，显示需要的页面

monkey.patch_all()

class HTTPServer(object):
    def __init__(self,port):
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #设置当服务器先close即服务器端4次挥手之后资源能够立即释放，这样就保证了下次开启服务可以立即使用8080端口
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
        self.server_socket.bind(('',port))
        self.server_socket.listen(128)
    
    def run(self):
        while True:
            web_socket,web_addr = self.server_socket.accept()
            # web_thread = threading.Thread(target=self.client_handle_msg,args=(web_socket,))
            # web_thread.start()

            #创建一个协程去处理接收到的消息
            gevent.spawn(self.client_handle_msg,web_socket)
            
            #self.client_handle_msg(web_socket)

    def client_handle_msg(self,web_socket):
        "处理客户端的请求信息"
        req = web_socket.recv(1024).decode("utf-8")
        req_lines = req.splitlines()
        for lines in req_lines:
            print(lines)

        http_req_line = req_lines[0]
        #http_req_line -->  'GET /favicon.ico HTTP/1.1'
        ret = re.match("([^/]*) ([^ ]*)",http_req_line)
        method = ret.group(1)

        get_file_name = ret.group(2)
        print("get file name is ======>%s"%get_file_name)

        #读取静态文件
        if get_file_name == "/":
            get_file_name = get_document_root + "/index.html"
        else:
            get_file_name = get_document_root + get_file_name
        print("get file name 2 is ==> %s" % get_file_name)

        try:
            f = open(get_file_name,"rb")
            resp_body = f.read()
            f.close()
        except Exception as e:
            #反馈失败信息，访问文件不存在
            resp_headers = "HTTP/1.1 404 NOT Found\r\n"
            resp_headers += "\r\n"
            resp_body = "sorry,your pages are not found...".encode()
        else:        
            #组织响应信息
            resp_headers = "HTTP/1.1 200 OK\r\n"
            resp_headers += "\r\n"

        finally:
            web_socket.send(resp_headers.encode() + resp_body)

            web_socket.close()
#设置服务器请求静态资源时的路径
get_document_root = "./templates"

def main():
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    else:
        print("[请以python3 xxx.py 端口号]来运行程序")
        return

    new_server = HTTPServer(port)
    new_server.run()    

if __name__ == '__main__':
    main()
    
    