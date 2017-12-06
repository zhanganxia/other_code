import socket
import feigeglobal
import threading
import feigerecv
import feigesend


#记录发送文件列表信息
send_file_list = list()

#处理飞秋请求文件的信息
def handle_request_file_info(request_file_info):
    #1.切割字符串
    request_file_info_list = request_file_info.split(":", 3)
    #2.将切割信息封装到字典
    file_info_dict = dict()
    #消息的包编号
    file_info_dict["packageid"] = int(request_file_info_list[0],16)
    #文件序号
    file_info_dict["fileindex"] = int(request_file_info_list[1])
    
    return file_info_dict
    
#接收客户端的请求信息
def recv_client_data(service_client_socket):
    
    #接收客户端的请求数据
    recv_data = service_client_socket.recv(1024)
    #处理接收数据封装到字典
    recv_info_dict = feigerecv.handle_recv_data(recv_data)
    #获取飞秋请求文件的信息
    request_file_info = recv_info_dict["content"]
    #处理飞秋请求的文件信息封装到字典
    file_info_dict = handle_request_file_info(request_file_info)

    print(file_info_dict)
    #遍历发送文件列表信息，然后根据飞秋请求文件信息获取文件名
    for current_file_dict in send_file_list:
        if (current_file_dict["packageid"] == file_info_dict["packageid"] and 
            current_file_dict["fileindex"] == file_info_dict["fileindex"]):
            #找到对应的文件信息，获取对应的文件名
            filename = current_file_dict["filename"]
            try:
                with open(filename,"rb") as file:
                    while True:
                        #获取每次读取的文件的二进制数据
                        file_data = file.read(1024)
                        if file_data:
                            #发送文件二进制数据
                            service_client_socket.send(file_data)
                        else:
                            break
            except Exception as e:
                print("文件发送异常：",e)
            else:
                print("%s文件发送成功"%filename)
            #print(filename)
            break

    #解码
    #recv_content = recv_data.decode("gbk")
    
    #经运行，点击下载，客户端的请求数据recv_content的结果是：1@shiyeline:18521:Administra:DEEP-17101:96:59f47cab:0:0:
    #请求接收的数据包括-->版本号：包编号：用户名：主机名：命令字96(表示下载文件)：16进制的包编号：文件序号：从哪个位置开始
    #recv_content:1@shiyeline:208255:Administra:DEEP-17101:96:59f6eac6:0:0:
    #print(recv_content)
    #关闭服务于客户端的socket
    service_client_socket.close()

#下载文件
def download_file(download_file_dict):
    #创建tcp客户端socket
    tcp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #建立链接
    tcp_client_socket.connect((download_file_dict["dest_ip"],feigeglobal.feiq_port))
    #发送请求下载文件基本信息
    file_info = "%x:%d:0"%download_file_dict["packageid"],download_file_dict["fileindex"]
    #生成下载文件的请求信息
    send_content = feigesend.build_msg(feigeglobal.IPMSG_GETFILEDATA,file_info)
    #生成下载文件的请求信息
    tcp_client_socket.send(send_content.encode("gbk"))
    #获取文件名
    filename = download_file_dict["filename"]

    #记录当前获取的文件二进制数据的大小
    currrnt_file_size = 0
    try:
        with open(filename,"wb") as file:
            while True:
                #接收飞秋给你发送的文件的二进制数据
                file_data = tcp_client_socket.recv(1024)
                if file_data:
                    #把获取的文件二进制数据写入到指定文件
                    file.write(file_data)                        
                    #记录每次获取的文件二进制的大小
                    current_file_size += len(file_data)
                else:
                    break
                #判断是否接收完成,如果接收的数据和原始数据的大小一致
                if current_file_size == download_file_dict["filesize"]:
                    break
    except Exception as e:
        print("文件下载出现异常:",e)
    else:
        print("%s文件下载成功"%filename)
    tcp_client_socket.close()
    
#接收队列的消息
def recv_queue_data(file_queue):
    while True:
        #获取文件的字典信息
        file_dict = file_queue.get()
        #判断接收数据文件类型
        if file_dict["type"] == "sendfile": 
            #保存发送文件列表
            send_file_list.append(file_dict["data"])
            print(send_file_list)
        elif file_dict["type"] == "downloadfile":
            #保存下载文件列表
            download_file_dict = file_dict["data"]

            #下载文件
            download_file(download_file_dict)
            


#if __name__ == '__main__':
def tcp_server_main(file_queue):
    #创建子线程来获取队列消息
    recv_queue_data_thread = threading.Thread(target = recv_queue_data,args=(file_queue,))
    recv_queue_data_thread.start()

    #创建socket
    tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #程序退出立即释放端口
    tcp_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
    #绑定端口
    tcp_server_socket.bind(("",feigeglobal.feiq_port))
    #设置监听，将套接字变为被动套接字
    tcp_server_socket.listen(128)
    #因为要不断的从客户端拿数据，所以要多次循环
    while True:        
        #等待客户端链接，服务于客户端
        service_client_socket,ip_port = tcp_server_socket.accept()
        #开辟线程服务客户端，接收客户端请求信息
        recv_thread = threading.Thread(target=recv_client_data,args=(service_client_socket,))
        recv_thread.start()

        # #接收客户端的请求数据
        # recv_data = service_client_socket.recv(1024)
        # #解码
        # recv_content = recv_data.decode("gbk")
        # print("recv_content")





