import socket

def send_msg(udp_socket):
    """获取键盘数据，并将其发送给对方"""
    #1.从键盘输入数据
    msg = input("请输入你要发送的数据")

    #2.请输入你要发送的IP
    dest_ip = input("\n请输入对方的ip地址")

    #3.输入对方的port
    dest_port = int(input("\n请输入对方的port："))

    #4.发送函数
    udp_socket.sendto(msg.encode(),(dest_ip,dest_port))

def recv_msg(udp_socket):
    #1.接收用户信息
    recv_msg = udp_socket.recvfrom(4098)
    #2.解码
    recv_ip = recv_msg[1]
    recv_msg = recv_msg[0].decode()
    #3.显示信息
    print(">>>%s:%s"%(str(recv_ip),recv_msg))

def main():
    #1.创建套接字
    udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    #广播群发，IP地址输入:255.255.255.255  端口：8080
    udp_socket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
    #2.绑定本地信息
    #udp_socket.bind("",8888)
    while True:
        #3.选择功能
        print("="*30)
        print("1.发送消息")
        print("2.接收消息")
        print("="*30)
        op_num = input("请输入要操作的功能序号：")

        #4.根据选择调用相应的函数
        if op_num == "1":
            send_msg(udp_socket)
        elif op_num == "2":
            recv_msg(udp_socket)
        else:
            print("输入有误，请重新输入。。。")

if __name__ == "__main__":
    main()
        

        
        


