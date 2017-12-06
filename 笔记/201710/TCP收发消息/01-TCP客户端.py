import socket
import time 

#创建TCP套接字
tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#拨号 -- 连接服务器
tcp_socket.connect(('192.168.20.80',8888))

#发数据
#send 就是发送数据使用的，返回值就是成功发送的数据<了解>
data = input("请输入要发送的数据：")
tcp_socket.send(data.encode("gbk"))

#收数据
#参数是本次收数据的最大长度  返回值就是收到bytes类型的数据
#如果没有收到数据 就会一直阻塞等待
#如果对方关掉该socket 那么我们将会收到一个0字节的数据
recv_data = tcp_socket.recv(4096)
if recv_data:
    print("收数据：%s" % recv_data.decode("gbk"))
else:
    print("对方已经关闭连接")

time.sleep(1000)
#关闭套接字
tcp_socket.close()
