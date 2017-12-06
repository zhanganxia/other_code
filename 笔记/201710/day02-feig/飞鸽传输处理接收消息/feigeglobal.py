#全局变量模块

#版本号
feiq_version = 1
#用户名
feiq_username = "安琪拉宝宝"
#主机名
feiq_hostname = "kkxiami"
#online_commond = 1

#上线
IPMSG_BR_ENTRY = 0x00000001
#offline_commond = 2
#下线
IPMSG_BR_EXIT = 0x00000002
# 通报在线
IPMSG_ANSENTRY = 0x00000003
#发送消息
IPMSG_SENDMSG = 0x00000020
# 告知对方收到消息
IPMSG_RECVMSG = 0x00000021
#广播地址
feiq_broadcast = '255.255.255.255'
#端口号
feiq_port = 2425
#全局socket
udp_client_socket = None