# 程序入口模块
import socket
import feigeglobal
import feigesend
import feigerecv
import threading
import multiprocessing
import feigetcp


# 创建socket
def create_socket():
    # 创建socket
    feigeglobal.udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 设置广播选项-> 开启广播选项支持发送广播消息
    # 1. 设置当前socket(udp_client_socket)
    # 2. 广播选项参数
    # 3. 是否开启广播
    feigeglobal.udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
    # 绑定端口
    feigeglobal.udp_client_socket.bind(("", feigeglobal.feiq_port))


# 显示在线用户列表信息
def show_online_user_list():
    print("------------在线列表用户信息--------------")
    for i, current_user_dict in enumerate(feigeglobal.online_user_list):
        print(i, current_user_dict)
    print("----------------------------------------")

#显示下载文件的列表信息
def show_download_file_list():
    print("------------下载文件列表信息--------------")
    for i,current_file_dict in enumerate(feigeglobal.download_file_list):
        print(i,current_file_dict)
    print("----------------------------------------")


# 显示飞鸽的功能菜单
def show_menu():
    print("      飞鸽传书")
    print("1: 上线")
    print("2: 下线")
    print("3: 给对方ip发送消息")
    print("4: 显示在线用户列表信息")
    print("5: 给对方ip发送文件")
    print("6: 显示下载文件的列表信息")
    print("7: 下载指定文件")
    print("0: 退出")
    return input("请输入功能选项:")


if __name__ == '__main__':

    # 创建文件的消息队列
    feigeglobal.file_queue = multiprocessing.Queue()

    # 创建tcp子进程，提供tcpsocket服务端
    tcp_process = multiprocessing.Process(target=feigetcp.tcp_server_main, args=(feigeglobal.file_queue,))
    # 守护主进程， 主进程退出后，子进程直接销毁
    tcp_process.daemon = True
    tcp_process.start()

    # 创建socket
    create_socket()

    # 创建子线程， 目的接收飞秋给你发送的消息
    recv_thread = threading.Thread(target=feigerecv.recv_msg)
    # 设置守护主线程，主线程退出后，子线程直接销毁不再执行代码
    recv_thread.setDaemon(True)
    recv_thread.start()

    # 显示功能菜单
    while True:
        menu_option = show_menu()
        if menu_option == "1":
            # 发送上线广播消息
            feigesend.send_online_msg()
        elif menu_option == "2":
            # 发送下线广播消息
            feigesend.send_offline_msg()
        elif menu_option == "3":
            # 给对方ip发送消息
            feigesend.send_msg_to_destip()
        elif menu_option == "4":
            # 显示在线用户列表信息
            show_online_user_list()
        elif menu_option == "5":
            feigesend.send_file_msg()
        elif menu_option == "6":
            #显示下载文件列表信息
            show_download_file_list()
        elif menu_option == "7":
            #下载文件
            feigesend.send_download_file_msg()
            pass
        elif menu_option == "0":
            # 发送下线广播消息
            feigesend.send_offline_msg()
            break

    # 关闭socket
    feigeglobal.udp_client_socket.close()
