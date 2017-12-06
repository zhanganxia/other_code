from socket import *

#1.创建socket
tcp_client_socket = socket(AF_INET,SOCK_STREAM)

#2.目的信息
server_ip = input("请输入服务器的ip：")
server_port = int(input("请输入服务器port:"))

#3.链接服务器
tcp_client_socket.connect((server_ip,server_port))

#4.提示用户输入数据
send_data = input("请输入要发送的数据：")

#5.发送数据
tcp_client_socket.send(send_data.encode("gbk"))

#6.接收对方发送过来的数据，最大接收1024字节
recvData = tcp_client_socket.recv(1024)
print('接收到的数据为：',recvData.decode('gbk'))

#关闭套接字
tcp_client_socket.close()

