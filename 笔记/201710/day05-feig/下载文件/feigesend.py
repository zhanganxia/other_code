#发送数据模块
import feigeglobal
import time
#import main
import main
import os


#生成发送消息内容
def build_msg(command,content=""):
    #记录每次生成的消息的包编号
    feigeglobal.packgeid = int(time.time())

    #准备发送消息
    send_content = "%d:%d:%s:%s:%d:%s" % (feigeglobal.feiq_version, feigeglobal.packgeid,
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

#给对方发送文件消息
def send_file_msg():
    #接收用户输入的对方ip地址
    dest_ip = input("请输入对方ip地址(输入0显示在线用户列表)")
    if dest_ip == "0":
        #显示在线用户列表
        main.show_online_list()
        try:
            #接收用户输入的序号
            index = int(input("请输入用户的序号："))
            #根据用户的序号获取列表中的字典信息
            user_dict = feigeglobal.online_user_list[index]
            #根据字典里面key获取对方的ip地址
            dest_ip = user_dict["destip"]
        except Exception as e:
            print("请输入合法的用户序号！")
            print("异常信息为：",e)
            return

        #接收用户发送的内容
    filename = input("请输入要发送的文件名：")
    if dest_ip and filename:
        #准备发送文件消息内容
        #版本号：包编号：用户名：主机名：命令字：消息\0文件序号:文件名:文件大小：文件修改时间：文件类型
        #这里我们只匹配消息后面的内容：消息\0文件序号:文件名:文件大小：文件修改时间：文件类型
        #获取文件大小
        file_size = os.path.getsize(filename)
        file_time = int(os.path.getctime(filename))
        
        file_info = "\0%d:%s:%x:%x:%x"%(0,filename,file_size,file_time,feigeglobal.IPMSG_FILE_REGULAR)
        send_file_info = build_msg(feigeglobal.IPMSG_SENDMSG | feigeglobal.IPMSG_FILEATTACHOPT,file_info)
        #send_file_info的内容：1:1509181309:安琪拉宝宝:kkxiami:2097184:0:feige.py:123:123124:1
        #print(send_file_info)
        #发送消息内容
        send_msg(send_file_info,dest_ip)

        #将文件包编号，文件序号，文件名封装到字典
        send_file_dict = dict()
        send_file_dict["packageid"] = feigeglobal.packgeid
        send_file_dict["fileindex"] = 0
        send_file_dict["filename"] = filename

        print(send_file_dict)
        #封装发送文件信息到字典
        file_dict = dict()
        #文件类型
        file_dict["filetype"] = "sendfile"
        file_dict["data"] = send_file_dict

        #将发送文件的字典信息放入消息队列
        feigeglobal.file_queue.put(file_dict) 

        #file_size = os.path.getsize(filename)
        #获取文件的修改的时间
        #file_change_time = int(os.path.getctime(filename))

#发送下载文件信息
def send_download_file_msg():
    #显示下载文件列表信息
    main.show_file_list()
    try:
        #接收用户输入的文件序号
        fileindex = int(input("请输入文件序号:"))
        #根据文件序号,获取对应下载文件的字典信息
        download_file_dict = feigeglobal.download_file_list[fileindex]
        print(download_file_dict)

        #封装下载文件信息到字典
        file_dict = dict()
        #文件类型
        file_dict["filetype"] = "downloadfile"
        #文件内容
        file_dict["data"] = download_file_dict

        #将下载文件字典信息放入消息队列
        feigeglobal.file_queue.put(file_dict)


    except Exception as e:
        print("请输入合法的文件序号:",e)



