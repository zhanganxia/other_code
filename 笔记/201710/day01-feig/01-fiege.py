#发送广播上线消息
import socket

if __name__ == '__main__':
    #创建socket
    udp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    #设置广播选项-->开启广播选项支持发送广播消息
    udp_client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,True)

    #准备发送上线广播消息:
    send_content = "1:12345678:itcast-python:localhost:1:hello!"

    #发送上线消息
    udp_client_socket.sendto(send_content.encode("gbk"),("255.255.255.255",2425))

    #关闭socket
    udp_client_socket.close()
