import feiglobal

def recv_msg():
    while True:
        recv_data,ip_port = feiglobal.udp_client_socket.recvfrom(1024)
        #解码
        reccv_content = recv_data.decode("gbk")
        print("*"*20)
        print(reccv_content,ip_port)