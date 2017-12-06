import socket

def get_file_data(file_name):
    #取本地查找文件 读取文件数据
    content = None
    try:
        with open("1.txt","rb") as file:
            content = file.read()
    except FileNotFoundError as e:
        pass
    finally:
        return content

#创建一个本地套接字  绑定  监听
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_socket.bind(('',8888))

server_socket.listen(128)
#接收用户请求获取到客户端套接字
client_socket,client_addr = server_socket.accept()
#收文件名
file_name = client_socket.recv(4096)

data = get_file_data("1.txt")
if data:
    client_socket.send(data)

#发送 完成后 关闭客户端套接字
client_socket.close()

#最后关闭服务器端套接字
server_socket.close()






