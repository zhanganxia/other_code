import socket
import re
#web静态页面，显示需要的页面

def client_handle_msg(web_socket):
    #req未进行decode -->输出的是二进制文件，以b开头 --> b'GET / HTTP/1.1'
    #req进行decode --> 输出的是字符串<class 'str'> ---> GET / HTTP/1.1
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
        #因为在组织请求头信息的时候，是按照字符串组织的，不能与读取的二进制文件合并，所以组织的头信息需要先encode为二进制
        #resp_header = resp_headers.encode("utf-8")
        #resp = resp_headers.encode() + resp_body
        web_socket.send(resp_headers.encode() + resp_body)

        web_socket.close()
#设置服务器请求静态资源时的路径
get_document_root = "./templates"

def main():
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #设置当服务器先close即服务器端4次挥手之后资源能够立即释放，这样就保证了下次开启服务可以立即使用8080端口
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
    server_socket.bind(('',8080))
    server_socket.listen(128)

    while True:
        web_socket,web_addr = server_socket.accept()
        client_handle_msg(web_socket)

if __name__ == '__main__':
    main()
    
    