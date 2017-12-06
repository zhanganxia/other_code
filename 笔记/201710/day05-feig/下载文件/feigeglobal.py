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
# 文件消息
IPMSG_FILEATTACHOPT = 0x00200000
# 普通文件
IPMSG_FILE_REGULAR = 0x00000001
# 文件消息
IPMSG_FILEATTACHOPT = 0x00200000
#下载文件
IPMSG_GETFILEDATA = 0x00000060
#广播地址
feiq_broadcast = '255.255.255.255'
#端口号
feiq_port = 2425
#全局socket
udp_client_socket = None

#保存在线用户信息列表
online_user_list = list()

#下载文件列表
download_file_list = list()

#消息编号
packgeid = None

#消息队列
file_queue = None

