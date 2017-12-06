#接收消息模块
import feigeglobal
import feigesend

#处理接收的飞秋数据
def handle_recv_data(recv_data):
    #decode解码部分飞秋发过来的消息解码不了，需要使用”errors = "ignore"这个参数
    recv_content = recv_data.decode("gbk",errors = "ignore")
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

#处理保存在线用户信息的逻辑
def handle_save_online_user_info(username,destip):
    #判断用户名和ip是否在在线列表里面，如果在不添加，否则就添加
    for current_user_dict in feigeglobal.online_user_list:
        if current_user_dict["username"] == username and current_user_dict["destip"] == destip:
            #在线列表里面有此用户，执行break后执行else 语句
            break
    else:
        #把用户名和用户ip保存到字典中
        online_user_dict = dict()
        online_user_dict["username"] = username
        online_user_dict["destip"] = destip
        feigeglobal.online_user_list.append(online_user_dict)

#删除下线用户信息
def remove_offline_user_info(destip):
    for current_user_dict in feigeglobal.online_user_list:
        if current_user_dict["destip"] == destip:
            feigeglobal.online_user_list.remove(current_user_dict)            
            break

def recv_msg():
    while True:
        recv_data,ip_port = feigeglobal.udp_client_socket.recvfrom(1024)
        recv_info_dict = handle_recv_data(recv_data)
        command,command_option = handle_command_num(recv_info_dict["command_num"])
        #print(command,command_option)
        if command == feigeglobal.IPMSG_BR_ENTRY:
            #上线
            print("%s上线了!"%recv_info_dict["username"])
            # #把用户名和用户ip保存到字典中
            # online_user_dict = dict()
            # online_user_dict["username"] = recv_info_dict["username"]
            # online_user_dict["destip"] = ip_port[0]

            # feigeglobal.online_user_list.append(online_user_dict)
            handle_save_online_user_info(recv_info_dict["username"],ip_port[0])

            feigesend.send_answer_msg(ip_port[0])
        elif command == feigeglobal.IPMSG_BR_EXIT:
            #下线
            print("---%s下线了---"%recv_info_dict["username"])
            remove_offline_user_info(ip_port[0])

        elif command == feigeglobal.IPMSG_ANSENTRY:
            #通报对方在线
            print("***%s已在线***"%recv_info_dict["username"])
            # online_user_dict = dict()
            # online_user_dict["username"] = recv_info_dict["username"]
            # online_user_dict["destip"] = ip_port[0]
            # feigeglobal.online_user_list.append(online_user_dict)
            handle_save_online_user_info(recv_info_dict["username"],ip_port[0])

        elif command == feigeglobal.IPMSG_SENDMSG:
            #判断接收到的消息是否是文件消息
            if command_option & 0x00f00000 == feigeglobal.IPMSG_FILEATTACHOPT:
                #保存下载文件的基本信息
                download_file_dict = dict()
                #消息的包编号
                download_file_dict["packageid"] = int(recv_info_dict["packageid"])
                #获取文件的消息内容
                file_info = recv_info_dict["content"]
                #找到"\0"这个位置
                zero_position = file_info.find("\0")
                #使用切片获取文件信息
                last_file_info = file_info[zero_position+1:]
                #根据":"分割字符串
                file_info_list = last_file_info.split(":",5)

                #文件序号
                download_file_dict["fileindex"] = file_info_list[0]
                #文件名
                download_file_dict["filename"] = file_info_list[1]
                #文件大小
                download_file_dict["filesize"] = int(file_info_list[2],16)
                #对方ip
                download_file_dict["dest_ip"] = ip_port[0]
                #print(download_file_dict)
                #保存下载文件的字典信息到列表
                feigeglobal.download_file_list.append(download_file_dict)
                print(feigeglobal.download_file_list)
                print("文件消息")
            else:
                #接收消息
                print("收到消息：%s"%recv_info_dict["content"])
            
            feigesend.send_tell_msg(ip_port[0])

            


