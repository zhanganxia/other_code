import socket
import feiglobal
import feigrecv
import feigsendmsg
import threading

def show_menu():
    print("请选择功能选项：")
    print("1.上线")
    print("2.下线")
    print("3.发送消息")
    print("4.接收消息")
    print("0.退出")
    return input("请输入：")

def creat_socket():
    global udp_client_socket
    #创建socket套接字
    udp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	#设置广播选项
    udp_client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,True)
    udp_client_socket.bind(('',feiglobal.feig_port))

if __name__ == '__main__':
    creat_socket()   
    recv_thread = threading.Thread(target=feigrecv.recv_msg)
    #设置守护线程
    recv_thread.setDaemon(True)
    #开启线程
    recv_thread.start()
    while True:
        menu_option = show_menu()
        if menu_option == "1":
            #发送上线广播消息
            feigsendmsg.send_online_msg()
        elif menu_option == "2":
            #发送下线广播消息
            feigsendmsg.send_offline_msg()
        elif menu_option == "3":
            #向指定ip发送消息
            feigsendmsg.send_msg_to_destip()
        elif menu_option == "4":
            #接收消息
            feigrecv.recv_msg()
        elif menu_option == "0":
            feigsendmsg.send_offline_msg()
            break
    udp_client_socket.close()