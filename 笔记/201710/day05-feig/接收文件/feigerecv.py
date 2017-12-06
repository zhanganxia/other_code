# 接收数据模块
import feigeglobal
import feigesend


# 处理接收的飞秋数据
def handle_recv_data(recv_data):
    # 解码
    recv_content = recv_data.decode("gbk", errors="ignore")
    # 1_lbt6_0#128#000C29DCD6D7#0#0#0#4001#9:1508920396:Apple:WIN-SMFIBLTAL72:6291459:Apple
    # 1.按照冒号切割
    # 2.切割次数
    recv_info_list = recv_content.split(":", 5)
    # 把列表数据封装到字典里面
    recv_info_dict = dict()
    # 版本号
    recv_info_dict["version"] = recv_info_list[0]
    # 消息的包编号
    recv_info_dict["packageid"] = recv_info_list[1]
    # 用户名
    recv_info_dict["username"] = recv_info_list[2]
    # 主机名
    recv_info_dict["hostname"] = recv_info_list[3]
    # 命令字
    recv_info_dict["command_num"] = recv_info_list[4]
    # 命令字对应消息内容
    recv_info_dict["content"] = recv_info_list[5]
    return recv_info_dict


# 提取命令字里面的命令及命令选项
def handle_command_num(command_num):
    # 使用按位与 提取命令及命令选项
    # 本质： 就是2个二进制数据进行按位与
    # 把第一个十进制转成二进制然后把16进制转成二进制，然后使用二进制进行按位与
    command = int(command_num) & 0x000000ff
    # 提取命令选项
    command_option = int(command_num) & 0xffffff00
    return command, command_option


# 处理保存在线用户信息的逻辑
def handle_save_online_user_info(username, destip):

    # 判断用户名和ip是否在在线列表里面，如果在不添加，否则就添加
    for current_user_dict in feigeglobal.online_user_list:
        if current_user_dict["username"] == username and current_user_dict["destip"] == destip:
            # 在线里面里面有该用户, 执行break不会执行else语句
            break
    else:
        # 把用户名和用户ip保存到字典里面
        online_user_dict = dict()
        # 用户名
        online_user_dict["username"] = username
        # 用户ip
        online_user_dict["destip"] = destip
        # 把在线用户信息保证到列表里面
        feigeglobal.online_user_list.append(online_user_dict)


# 删除下线用户信息
def remove_offline_user_info(destip):
    for current_user_dict in feigeglobal.online_user_list:
        if current_user_dict["destip"] == destip:
            # 找到下线用户信息了，然后删除它
            feigeglobal.online_user_list.remove(current_user_dict)
            break


# 接收消息
def recv_msg():
    while True:
        # 每次接收的最大字节数：1024
        recv_data, ip_port = feigeglobal.udp_client_socket.recvfrom(1024)
        # 处理接收的数据封装到字典里面
        recv_info_dict = handle_recv_data(recv_data)
        # 提取命令字里面的命令及命令选项
        command, command_option = handle_command_num(recv_info_dict["command_num"])
        if command == feigeglobal.IPMSG_BR_ENTRY:
            # 上线
            print("%s上线了" % recv_info_dict["username"])
            # 保存在线用户信息到列表
            handle_save_online_user_info(recv_info_dict["username"], ip_port[0])

            # 回复对方我也在线
            # send_content = feigesend.build_msg(feigeglobal.IPMSG_ANSENTRY, feigeglobal.feiq_username)
            # feigesend.send_msg(send_content, ip_port[0])
            feigesend.send_answer_msg(ip_port[0])

        elif command == feigeglobal.IPMSG_BR_EXIT:
            # 下线
            print("%s下线了" % recv_info_dict["username"])
            # 删除下线用信息
            remove_offline_user_info(ip_port[0])

        elif command == feigeglobal.IPMSG_ANSENTRY:
            # 对方通报在线
            print("%s已经在线" % recv_info_dict["username"])

            # 保存在线用户信息到列表
            handle_save_online_user_info(recv_info_dict["username"], ip_port[0])

        elif command == feigeglobal.IPMSG_SENDMSG:
            #判断是否是文件消息
            if command_option & 0x00f00000 == feigeglobal.IPMSG_FILEATTACHOPT:
                #保存下载文件的基本信息
                download_file_dict = dict()
                #消息的包编号
                download_file_dict["packageid"] = int(recv_info_dict["packageid"])
                #获取文件消息内容
                file_info = recv_info_dict["content"]
                #找到”\0“这个位置
                zero_position = file_info.find("\0")
                #s使用切片获取文件信息
                last_file_info = file_info[zero_position+1:]
                #根据”：“分割字符串
                file_info_list = last_file_info.split(":",5)
                #文件序号
                download_file_dict["fileindex"] = int(file_info_list[0])
                #文件名
                download_file_dict["filename"] = file_info_list[1]
                #文件大小
                download_file_dict["filesize"] = int(file_info_list[2],16)
                #对方ip
                download_file_dict["dest_ip"] = ip_port[0]
                #print(download_file_dict)
                #保存下载文件的字典信息
                feigeglobal.download_file_list.append(download_file_dict)

                print("文件消息")
            else:
                print("接收的消息为:%s" % recv_info_dict["content"])
            # 接收消息
            #print("接收的消息为:%s" % recv_info_dict["content"])
            # 生成发送的内容
            # send_content = feigesend.build_msg(feigeglobal.IPMSG_RECVMSG)
            # # 告知对方收到消息
            # feigesend.send_msg(send_content, ip_port[0])
            feigesend.send_tell_msg(ip_port[0])