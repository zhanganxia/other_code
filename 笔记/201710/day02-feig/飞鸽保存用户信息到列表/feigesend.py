#发送数据模块
import feigeglobal
import time
#import main
import main


#生成发送消息内容
def build_msg(command,content=""):
    #准备发送消息
    send_content = "%d:%d:%s:%s:%d:%s" % (feigeglobal.feiq_version, int(time.time()),
                                              feigeglobal.feiq_username, feigeglobal.feiq_hostname,
                                              command, content)
    return send_content

 #发送消息的通用函数
def send_msg(send_content,dest_ip):
        feigeglobal.udp_client_socket.sendto(send_content.encode("gbk"), (dest_ip, feigeglobal.feiq_port))


def send_online_msg():
    send_content = build_msg(feigeglobal.IPMSG_BR_ENTRY,feigeglobal.feiq_username)
    send_msg(send_content,feigeglobal.feiq_broadcast)

def send_offline_msg():
    send_content = build_msg(feigeglobal.IPMSG_BR_EXIT,feigeglobal.feiq_username)
    send_msg(send_content,feigeglobal.feiq_broadcast)

#回复对方我也在线
def send_answer_msg(destip):
    send_content = build_msg(feigeglobal.IPMSG_ANSENTRY,feigeglobal.feiq_username)
    send_msg(send_content,destip)

#回复对方我收到消息
def send_tell_msg(destip):
    #生成发送的内容
    send_content = build_msg(feigeglobal.IPMSG_RECVMSG)
    #告知对方收到消息了
    send_msg(send_content,destip)


def send_msg_to_destip():
    #接收用户输入的对方ip地址
    dest_ip = input("请输入对方ip地址(输入0显示在线用户列表):")
    if dest_ip == "0":
        main.show_online_list()
        try:           
            index = int(input("请输入序号："))
            user_dict = feigeglobal.online_user_list[index]
            dest_ip = user_dict["destip"]
        except Exception as e:
            print("请输入合法的序号！")
            print("打印异常信息！",e)
            return

    #接收用户发送的内容
    content = input("请输入发送的内容：")
    if dest_ip and content:
        send_content = build_msg(feigeglobal.IPMSG_SENDMSG,content)
        # 发送下线消息
        #udp_client_socket.sendto(send_content.encode("gbk"), (dest_ip, feiq_port))
        send_msg(send_content,dest_ip)