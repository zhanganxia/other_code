from socket import *

#连接上服务器
client_socket = socket(AF_INET,SOCK_STREAM)
server_ip = input("IP:")
server_port = int(input("port:"))
client_socket.connect((server_ip,server_port))

#输入下载文件的名称
file_name = input("请输入你要下载的文件名称：")

#将收到文件名发送给服务器
client_socket.send(file_name.encode())

#开始接收文件数据,打开文件用以保存文件数据
recv_data = client_socket.recv(4096)

with open(file_name,"wb") as file:
    file.write(recv_data)

#收完，关闭套接字
client_socket.close()