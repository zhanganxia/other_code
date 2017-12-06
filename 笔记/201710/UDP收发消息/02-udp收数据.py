import socket
# 创建UDP套接字            IPV4            UDP 用户数据报协议
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 使用
data = input("请输入你要发送的数据:")

# 发送数据需要送到的 目的地址(IP, port)
dest_address = ('192.168.20.116', 8080)
udp_socket.sendto(data.encode(), dest_address) #1024表示本次接收的最大字节

#等待接收对对方发送的数据
#recv_data = udp_socket.recvfrom(1024) #1024表示本次接收的最大字节数
data, remote_address = udp_socket.recvfrom(4096)
print("收到来自%s的数据:%s" % (str(remote_address), data))

# 记得关闭 10000个 10001一个进程所能打开的文件等系统资源是有限制的
# 使用系统资源  关闭套接字
#7.关闭套接字
udp_socket.close()
