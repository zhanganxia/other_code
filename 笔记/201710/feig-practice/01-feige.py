import socket
import time

feig_version = 1
feig_username = "test"
feig_hostname = "computer"
online_commond = 1
feig_broadcast = "255.255.255.255"
feig_port = 2425

if __name__ == '__main__':
    #创建socket套接字
	udp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	#设置广播选项
	udp_client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,True)
	#准备发送上线广播消息
	#send_content = "1:12345678:itcast-python:localhost:1:hello!"
	send_content = "%d:%d:%s:%s:%d:%s" %(feig_version,int(time.time()),
										feig_username,feig_hostname,
										online_commond,feig_username)
	#发送消息
	udp_client_socket.sendto(send_content.encode("gbk"),(feig_broadcast,feig_port))
	#关闭socket
	udp_client_socket.close()

    	
    	