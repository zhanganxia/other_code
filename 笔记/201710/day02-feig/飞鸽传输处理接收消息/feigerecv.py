#接收消息模块
import feigeglobal
import feigesend

#处理接收的飞秋数据
def handle_recv_data(recv_data):
    #decode解码部分飞秋发过来的消息解码不了，需要使用”errors = "ignore"这个参数
    recv_content = recv_data.decode("gbk",errors = "ignore")
    # 1_lbt6_0#128#000C29DCD6D7#0#0#0#4001#9:1508920396:Apple:WIN-SMFIBLTAL72:6291459:Apple
    #print(recv_content,ip_port)
    #1.按照冒号切割
    #2.切割次数
    recv_info_list = recv_content.split(":",5)
    #把列表数据封装到字典里面
    recv_info_dict = dict()
    #版本号
    recv_info_dict["version"] = recv_info_list[0]
    # 包编号  -->packageid
    recv_info_dict["packageid"] = recv_info_list[1]
    # 用户名  -->username
    recv_info_dict["username"] = recv_info_list[2]
    # 主机名  -->hostname
    recv_info_dict["hostname"] = recv_info_list[3]
    # 命令字  -->commond_num
    recv_info_dict["command_num"] = recv_info_list[4]
    # 命令字对应的消息内容  -->content
    recv_info_dict["content"] = recv_info_list[5]
    return recv_info_dict

# 提取命令字里面的命令及命令选项
def handle_command_num(command_num):
    command = int(command_num) & 0x000000ff
    command_option = int(command_num) & 0xffffff00
    return command,command_option


def recv_msg():
    while True:
        recv_data,ip_port = feigeglobal.udp_client_socket.recvfrom(1024)
        #解码
        # recv_content = recv_data.decode("gbk")
        # print("*"*20)
        # print(recv_content,ip_port)
        #处理接收的数据封装到字典里面
        recv_info_dict = handle_recv_data(recv_data)
        command,command_option = handle_command_num(recv_info_dict["command_num"])
        #print(command,command_option)
        if command == feigeglobal.IPMSG_BR_ENTRY:
            #上线
            print("%s上线了!"%recv_info_dict["username"])
            #回复对方我也在线(抽取到feigesend模块)
            # send_content = feigesend.build_msg(feigeglobal.IPMSG_ANSENTRY,feigeglobal.feiq_username)
            # feigesend.send_msg(send_content,ip_port[0])
            feigesend.send_answer_msg(ip_port[0])
        elif command == feigeglobal.IPMSG_BR_EXIT:
            #下线
            print("---%s下线了---"%recv_info_dict["username"])
        elif command == feigeglobal.IPMSG_ANSENTRY:
            #通报对方在线
            print("***%s已在线***"%recv_info_dict["username"])
        elif command == feigeglobal.IPMSG_SENDMSG:
            #接收消息
            print("收到消息：%s"%recv_info_dict["content"])
            
            # #生成发送的内容
            # send_content = feigesend.build_msg(feigeglobal.IPMSG_RECVMSG)
            # #告知对方收到消息了
            # feigesend.send_msg(send_content,ip_port[0])
            feigesend.send_tell_msg(ip_port[0])

            


