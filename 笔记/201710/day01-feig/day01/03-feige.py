# 添加飞鸽功能菜单选项

import socket
import time

# 版本号
feiq_version = 1
# 用户名
feiq_username = "hbin"
# 主机名
feiq_hostname = "macPro"
# 上线
online_command = 1
# 下线
offline_command = 2
# 广播地址
feiq_broadcast = "255.255.255.255"
# 端口号
feiq_port = 2425
# 全局socket
udp_client_socket = None


# 创建socket
def create_socket():
    global udp_client_socket
    # 创建socket
    udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 设置广播选项-> 开启广播选项支持发送广播消息
    # 1. 设置当前socket(udp_client_socket)
    # 2. 广播选项参数
    # 3. 是否开启广播
    udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)


# 发送上线广播消息
def send_online_msg():
    # 准备发送上线广播消息 # 1:123456789:itcast-python:localhost:1:hello
    send_content = "%d:%d:%s:%s:%d:%s" % (feiq_version, int(time.time()),
                                          feiq_username, feiq_hostname,
                                          online_command, feiq_username)
    # 发送上线消息
    udp_client_socket.sendto(send_content.encode("gbk"), (feiq_broadcast, feiq_port))


# 发送下线广播消息
def send_offline_msg():
    # 准备发送上线广播消息 # 1:123456789:itcast-python:localhost:2:hello
    send_content = "%d:%d:%s:%s:%d:%s" % (feiq_version, int(time.time()),
                                          feiq_username, feiq_hostname,
                                          offline_command, feiq_username)
    # 发送上线消息
    udp_client_socket.sendto(send_content.encode("gbk"), (feiq_broadcast, feiq_port))


# 显示飞鸽的功能菜单
def show_menu():
    print("      飞鸽传书")
    print("1: 上线")
    print("2: 下线")
    print("0: 退出")
    return input("请输入功能选项:")


if __name__ == '__main__':
    # 创建socket
    # udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # # 设置广播选项-> 开启广播选项支持发送广播消息
    # # 1. 设置当前socket(udp_client_socket)
    # # 2. 广播选项参数
    # # 3. 是否开启广播
    # udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)

    create_socket()

    # # 准备发送上线广播消息 # 1:123456789:itcast-python:localhost:1:hello
    # send_content = "%d:%d:%s:%s:%d:%s" % (feiq_version, int(time.time()),
    #                                       feiq_username, feiq_hostname,
    #                                       online_command, feiq_username)
    # # 发送上线消息
    # udp_client_socket.sendto(send_content.encode("gbk"), (feiq_broadcast, feiq_port))
    # 显示功能菜单
    while True:
        menu_option = show_menu()
        if menu_option == "1":
            # 发送上线广播消息
            send_online_msg()
        elif menu_option == "2":
            # 发送下线广播消息
            send_offline_msg()
        elif menu_option == "0":
            # 发送下线广播消息
            send_offline_msg()
            break

    # 关闭socket
    udp_client_socket.close()
