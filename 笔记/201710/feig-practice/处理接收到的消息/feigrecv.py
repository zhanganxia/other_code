import feiglobal
import feigsendmsg

#接收到的消息格式：1_lbt6_0#128#000C29DCD6D7#0#0#0#4001#9:1508920396:Apple:WIN-SMFIBLTAL72:6291459:Apple
def handle_recv_data(recv_data):
    #解码：
    recv_content = recv_data.decode("gbk")
    #按照冒号切割，并且把切割的数据封装到列表中
    recv_info_list = recv_content.split(":",5)
    #把列表数据封装到字典中
    recv_info_dict = dict()
    #版本号
    recv_info_dict["version"] = recv_info_list[0]
    #包编号
    recv_info_dict["packageid"] = recv_info_list[1]
    #用户名
    recv_info_dict["username"] = recv_info_list[2]
    #主机名
    recv_info_dict["hostname"] = recv_info_list[3]
    #命令字
    recv_info_dict["commond_num"] = recv_info_list[4]
    #消息内容
    recv_info_dict["content"] = recv_info_list[5]

    return recv_info_dict

#提取命令字里面的命令及命令选项
def handle_commond_num(commond_num):
    commond = int(commond_num) & 0x000000ff
    commond_opt = int(commond_num) & 0xffffff00
    return commond,commond_opt

def recv_msg():
    while True:
        recv_data,ip_port = feiglobal.udp_client_socket.recvfrom(1024)
        #解码
        # recv_content = recv_data.decode("gbk")
        # print("*"*20)
        recv_info_dict = handle_recv_data(recv_data)
        # print(recv_info_dict)
        commond,commond_opt = handle_commond_num(recv_info_dict["commond_num"])
        if commond == feiglobal.IPMSG_BR_ENTRY:
            print("%s上线了"%recv_info_dict["username"])
            #回复对方我也在线
            send_content = feigsendmsg.build_msg()
        elif commond == feiglobal.IPMSG_BR_EXIT:
            print("%s下线了"%recv_info_dict["username"])
        elif commond == feiglobal.IPMSG_ANSENTRY:
            print("%s已在线"%recv_info_dict["username"])
        elif commond ==feiglobal.IPMSG_SENDMSG:
            print("收到消息：%s"%recv_info_dict["content"])
             

