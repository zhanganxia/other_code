import socket
import time

feiq_version = 1
feiq_username = "zax"
feiq_hostname = "kkxiami"
online_commond = 1
offline_commond = 2
feiq_broadcast = '255.255.255.255'
feiq_port = 2435

udp_client_socket = None

def show_menu():
    print('请选择功能选项：')
    print('1.上线')
    print("2.下线")
    print("0.退出")
    return input("请输入选项：")

def creat_socket():
    global udp_client_socket
    udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 设置广播选项-->开启广播选项支持发送广播消息
    udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)

def send_offline_msg():
    # 准备发送下线广播消息:
    # send_content = "1:12345678:itcast-python:localhost:1:hello!"
    send_content = "%d:%d:%s:%s:%d:%s" % (feiq_version, int(time.time()),
                                          feiq_username, feiq_hostname,
                                          offline_commond, feiq_username)

    # 发送下线消息
    udp_client_socket.sendto(send_content.encode("gbk"), ("255.255.255.255", 2425))

def send_online_msg():
    # 准备发送上线广播消息:
    # send_content = "1:12345678:itcast-python:localhost:1:hello!"
    send_content = "%d:%d:%s:%s:%d:%s" % (feiq_version, int(time.time()),
                                          feiq_username, feiq_hostname,
                                          online_commond, feiq_username)

    # 发送上线消息
    udp_client_socket.sendto(send_content.encode("gbk"), ("255.255.255.255", 2425))

if __name__ == '__main__':
    creat_socket()
    while True:
        menu_option = show_menu()
        if menu_option == "1":
            #发送上线广播消息
            send_online_msg()
        elif menu_option == "2":
            #发送下线广播消息
            send_offline_msg()
        elif menu_option == "0":
            send_offline_msg()
            break

udp_client_socket.close()