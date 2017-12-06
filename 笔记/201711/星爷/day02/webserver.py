# 手写一个服务器: 能够接收浏览器的请求, 并且能够给浏览器发送固定的数据
import socket

text_content = """HTTP/1.1 200 OK
Content-Type:text/html

<html>
<head><h1>WOW</h1></head>
    <body>
        
        
        http://blog.csdn.net/q1302182594/article/details/51658229
        hahah1
    </body>
</html>

"""
if __name__ == '__main__':
    # 创建socket
    web_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 设置程序退出立即释放端口
    web_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # 套接字绑定地址
    web_server_socket.bind(('0.0.0.0', 8080))

    # 设置监听
    web_server_socket.listen(128)

    print("waiting for connection...")
    while True:
        # 接受客户端的连接
        webClisock, addr = web_server_socket.accept()

        print("connected from:", addr)
        webClisock.send(text_content.encode("utf-8"))
        webClisock.close()
    web_server_socket.close()
