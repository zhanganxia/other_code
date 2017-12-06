#发送广播上线消息
import socket
import time


feiq_version = 1
feiq_username = "zax"
feiq_hostname = "kkxiami"
online_commond = 1
feiq_broadcast = '255.255.255.255'
feiq_port = 2435

if __name__ == '__main__':
    #创建socket
    udp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    #设置广播选项-->开启广播选项支持发送广播消息
    udp_client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,True)

    #准备发送上线广播消息:
    #send_content = "1:12345678:itcast-python:localhost:1:hello!"
    send_content = "%d:%d:%s:%s:%d:%s"%(feiq_version,int(time.time()),
                                        feiq_username,feiq_hostname,
                                        online_commond,feiq_username)

    #发送上线消息
    udp_client_socket.sendto(send_content.encode("gbk"),("255.255.255.255",2425))

    #关闭socket
    udp_client_socket.close()
