#接收消息模块
import feigeglobal

def recv_msg():
    while True:
        recv_data,ip_port = feigeglobal.udp_client_socket.recvfrom(1024)
        #解码
        recv_content = recv_data.decode("gbk")
        print("*"*20)
        print(recv_content,ip_port)