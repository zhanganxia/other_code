#encoding=utf-8
import socket
import time

#版本号
feiq_version = 1
#用户名
feiq_username = "zax"
#主机名
feiq_hostname = "kkxiami"
#online_commond = 1

#上线
IPMSG_BR_ENTRY = 0x00000001
#offline_commond = 2
#下线
IPMSG_BR_EXIT = 0x00000002
#发送消息
IPMSG_SENDMSG = 0x00000020
#广播地址
feiq_broadcast = '255.255.255.255'
#端口号
feiq_port = 2425
#全局socket
udp_client_socket = None

def show_menu():
    print('请选择功能选项：')
    print('1.上线')
    print("2.下线")
    print("3.发送消息")
    print("0.退出")
    return input("请输入选项：")

def send_msg_to_destip():
    #接收用户输入的对方ip地址
    dest_ip = input("请输入对方ip地址")
    #接收用户发送的内容
    content = input("请输入发送的内容：")
    if dest_ip and content:
        #准备发送消息
        send_content = "%d:%d:%s:%s:%d:%s" % (feiq_version, int(time.time()),
                                              feiq_username, feiq_hostname,
                                              IPMSG_SENDMSG, content)
        # 发送下线消息
        udp_client_socket.sendto(send_content.encode("gbk"), (dest_ip, feiq_port))


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
                                         IPMSG_BR_EXIT, feiq_username)

    # 发送下线消息
    udp_client_socket.sendto(send_content.encode("gbk"), (feiq_broadcast,feiq_port))

def send_online_msg():
    # 准备发送上线广播消息:
    # send_content = "1:12345678:itcast-python:localhost:1:hello!"
    send_content = "%d:%d:%s:%s:%d:%s" % (feiq_version, int(time.time()),
                                          feiq_username, feiq_hostname,
                                          IPMSG_BR_ENTRY, feiq_username)

    # 发送上线消息
    udp_client_socket.sendto(send_content.encode("gbk"), (feiq_broadcast, feiq_port)

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
        elif menu_option == "3":
            send_msg_to_destip()

        elif menu_option == "0":
            send_offline_msg()
            break

udp_client_socket.close()