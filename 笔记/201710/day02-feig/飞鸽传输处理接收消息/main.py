#程序入口模块
import socket
import time
import feigerecv
import feigesend
import feigeglobal
import threading

# 创建socket
def create_socket():
    global udp_client_socket
    # 创建socket
    feigeglobal.udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 设置广播选项-> 开启广播选项支持发送广播消息
    # 1. 设置当前socket(udp_client_socket)
    # 2. 广播选项参数
    # 3. 是否开启广播
    feigeglobal.udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
    # 绑定端口
    feigeglobal.udp_client_socket.bind(("",feigeglobal.feiq_port))
def show_menu():
    print('请选择功能选项：')
    print('1.上线')
    print("2.下线")
    print("3.发送消息")
    #print("4.接收消息")
    print("0.退出")
    return input("请输入选项：")

if __name__ == '__main__':
    #创建socket
    create_socket()
    #创建子线程
    recv_thread = threading.Thread(target=feigerecv.recv_msg)
    #设置守护主线程，主线程退出后，子线程直接销毁，不再执行代码
    recv_thread.setDaemon(True)
    recv_thread.start()

    while True:
        menu_option = show_menu()
        if menu_option == "1":
            #发送上线广播消息
            feigesend.send_online_msg()
        elif menu_option == "2":
            #发送下线广播消息
            feigesend.send_offline_msg()
        elif menu_option == "3":
            feigesend.send_msg_to_destip()
        # elif menu_option == "4":
        #     feigerecv.recv_msg()
        #     print("*"*20)
        elif menu_option == "0":
            feigesend.send_offline_msg()
            break

feigeglobal.udp_client_socket.close()