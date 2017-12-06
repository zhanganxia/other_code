import socket
import time

feig_version = 1
feig_username = "test"
feig_hostname = "computer"
online_commond = 1
offline_commond = 2
feig_broadcast = "255.255.255.255"
feig_port = 2425
udp_client_socket = None

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

#抽取准备发送上线广播消息
def send_online_msg():
    send_content = "%d:%d:%s:%s:%d:%s" %(feig_version,int(time.time()),
										feig_username,feig_hostname,
										online_commond,feig_username)
	#发送上线广播消息
    udp_client_socket.sendto(send_content.encode("gbk"),(feig_broadcast,feig_port))

#下线广播消息
def send_offline_msg():
    send_content = "%d:%d:%s:%s:%d:%s" %(feig_version,int(time.time()),
										feig_username,feig_hostname,
										offline_commond,feig_username)
	#发送上线广播消息
    udp_client_socket.sendto(send_content.encode("gbk"),(feig_broadcast,feig_port))
    
def send_msg_to_destip():
    dest_ip = input("请输入对方的ip：")
    #ip_port = input("端口：")
    content = input("请输入要发送的内容：")
    if dest_ip and content:
        send_content = "%d:%d:%s:%s:%d:%s" %(feig_version,int(time.time()),
                                            feig_username,feig_hostname,
                                            offline_commond,feig_username)
        #发送上线广播消息
        udp_client_socket.sendto(send_content.encode("gbk"),(dest_ip,feig_port))

def recv_msg():
    while True:
        recv_data,ip_port = udp_client_socket.recvfrom(1024)
        #解码
        reccv_content = recv_data.decode("gbk")
        print("*"*20)
        print(reccv_content,ip_port)

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
            #向指定ip发送消息
            send_msg_to_destip()
        elif menu_option == "4":
            #接收消息
            recv_msg()
        elif menu_option == "0":
            send_offline_msg()
            break
    udp_client_socket.close()

    	
    	