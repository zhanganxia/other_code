import socket

#创建UDP套接字  IPV4   UDP用户数据报协议
udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#将本地端口8888占用  放弃操作系统随机分配
udp_socket.bind(('',8888))

#使用
data = input("请输入你要发送的数据：")

while True:
    data,remote_address = udp_socket.recvfrom(4096)
    print("收到来自%s的数据：%s"%(str(remote_address),data))

    udp_socket.sendto(data,remote_address)

udp_socket.close()


