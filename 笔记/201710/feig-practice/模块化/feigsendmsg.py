import feiglobal
import time

#抽取准备发送上线广播消息
def send_online_msg():
    send_content = "%d:%d:%s:%s:%d:%s" %(feiglobal.feig_version,int(time.time()),
										feiglobal.feig_username,feiglobal.feig_hostname,
										feiglobal.online_commond,feiglobal.feig_username)
	#发送上线广播消息
    feiglobal.udp_client_socket.sendto(send_content.encode("gbk"),(feiglobal.feig_broadcast,feiglobal.feig_port))

#下线广播消息
def send_offline_msg():
    send_content = "%d:%d:%s:%s:%d:%s" %(feiglobal.feig_version,int(time.time()),
										feiglobal.feig_username,feiglobal.feig_hostname,
										feiglobal.offline_commond,feiglobal.feig_username)
	#发送上线广播消息
    feiglobal.udp_client_socket.sendto(send_content.encode("gbk"),(feiglobal.feig_broadcast,feiglobal.feig_port))
    
def send_msg_to_destip():
    dest_ip = input("请输入对方的ip：")
    #ip_port = input("端口：")
    content = input("请输入要发送的内容：")
    if dest_ip and content:
        send_content = "%d:%d:%s:%s:%d:%s" %(feiglobal.feig_version,int(time.time()),
                                            feiglobal.feig_username,feiglobal.feig_hostname,
                                            feiglobal.offline_commond,feiglobal.feig_username)
        #发送上线广播消息
        feiglobal.udp_client_socket.sendto(send_content.encode("gbk"),(dest_ip,feiglobal.feig_port))
