#发送数据模块
import feigeglobal
import time

#生成发送消息内容
def build_msg(command,content):
    #准备发送消息
    send_content = "%d:%d:%s:%s:%d:%s" % (feigeglobal.feiq_version, int(time.time()),
                                              feigeglobal.feiq_username, feigeglobal.feiq_hostname,
                                              command, content)
    return send_content

 #发送消息的通用函数
def send_msg(send_content,dest_ip):
        feigeglobal.udp_client_socket.sendto(send_content.encode("gbk"), (dest_ip, feigeglobal.feiq_port))


def send_online_msg():
    # 准备发送上线广播消息:
    # send_content = "1:12345678:itcast-python:localhost:1:hello!"
    # send_content = "%d:%d:%s:%s:%d:%s" % (feiq_version, int(time.time()),
    #                                       feiq_username, feiq_hostname,
    #                                       IPMSG_BR_ENTRY, feiq_username)
    send_content = build_msg(feigeglobal.IPMSG_BR_ENTRY,feigeglobal.feiq_username)
    # 发送上线消息
    #udp_client_socket.sendto(send_content.encode("gbk"), (feiq_broadcast, feiq_port))
    send_msg(send_content,feigeglobal.feiq_broadcast)

def send_offline_msg():
    # 准备发送下线广播消息:
    # send_content = "1:12345678:itcast-python:localhost:1:hello!"
    # send_content = "%d:%d:%s:%s:%d:%s" % (feiq_version, int(time.time()),
    #                                       feiq_username, feiq_hostname,
    #                                      IPMSG_BR_EXIT, feiq_username)
    send_content = build_msg(feigeglobal.IPMSG_BR_EXIT,feigeglobal.feiq_username)
    # 发送下线消息
    #udp_client_socket.sendto(send_content.encode("gbk"), (feiq_broadcast, feiq_port))
    send_msg(send_content,feigeglobal.feiq_broadcast)

def send_msg_to_destip():
    #接收用户输入的对方ip地址
    dest_ip = input("请输入对方ip地址")
    #接收用户发送的内容
    content = input("请输入发送的内容：")
    if dest_ip and content:
        #准备发送消息
        # send_content = "%d:%d:%s:%s:%d:%s" % (feiq_version, int(time.time()),
        #                                       feiq_username, feiq_hostname,
        #                                       IPMSG_SENDMSG, content)
        send_content = build_msg(feigeglobal.IPMSG_SENDMSG,content)
        # 发送下线消息
        #udp_client_socket.sendto(send_content.encode("gbk"), (dest_ip, feiq_port))
        send_msg(send_content,dest_ip)