import socket
import time

#版本号
feiq_version = 1
#用户名
feiq_username = "kikixiami"
#主机名
feiq_hostname = "mypc"
#上线
online_commond = 1
#广播地址
feiq_broadcast = "255.255.255.255"
#端口号
feiq_port = 2425


if __name__ == '__main__':
    #创建socket
    udp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    #设置广播选项
    udp_client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,True)
    #准备发送上线广播消息 1:123456789:itcast-python:localhost:1:hello
    send_content = "%d:%d:%s:%s:%d:%s"%(feiq_version, int(time.time()),
                                        feiq_username, feiq_hostname,
                                        online_commond, feiq_username)
    #发送上线消息
    udp_client_socket.sendto(send_content.encode("gbk"),(feiq_broadcast,feiq_port))
    #关闭socket
    udp_client_socket.close()
