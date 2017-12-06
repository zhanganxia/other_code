import socket

#创建本地套接字 -- 总机
tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#绑定本地地址 -- 10086
tcp_socket.bind(('',8999))
#将套接字变为被动套接字 --安装一个前台的客户服务系统，并且设置等待服务器的大小
tcp_socket.listen(128)

#从等待服务区中取出一个客户套接字
#client_socket是客户端套接字，使用这个套接字和客户进行通信
#client_adr 是客户端地址，可以表示客户
while True:
    client_socket,client_addr = tcp_socket.accept()
    print("接收到来自%s的请求："% str(client_addr))

    # #echo 回射服务器
    recv_data = client_socket.recv(4096)
    if recv_data:
        print("收到来自%s的数据：%s" %(str(client_addr),recv_data))
        client_socket.send(recv_data)
    else:
        print("收到来自%s的断开请求：%s"%(str(client_addr),recv_data))
    client_socket.close()

tcp_socket.close()


