import socket
import re


def main():
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    tcp_server_socket.bind(('', 8080))
    tcp_server_socket.listen(128)
    while True:
        web_socket, web_addr = tcp_server_socket.accept()
        request = web_socket.recv(1024)
        print(request.decode('utf-8'))

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
        print(path)
        if path == "/":
            path = "/index.html"
        # 打开文件
        file = open("./html/html" + path, 'rb')
        # 读取二进制的数据
        content = file.read()
        file.close()

        response_header = "HTTP/1.1 200 OK\r\n"
        response_header += "\r\n"
        response_body = content

        response = response_header.encode() + response_body
        web_socket.send(response)
        # 断开连接
        web_socket.close()


if __name__ == '__main__':
    main()
