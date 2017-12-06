import socket
import time


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', 8080))
    server_socket.listen(128)
    # 设置套接字为非阻塞的状态
    server_socket.setblocking(False)

    socket_list = []
    while True:
        try:
            client_socket, client_addr = server_socket.accept()
        except Exception as ret:
            print("无客户端连接:", ret)
        else:
            print("新的客户端连接:", client_socket)
            socket_list.append(client_socket)
            client_socket.setblocking(False)
        for client_socket in socket_list:
            try:
                recvData = client_socket.recv(1024)
                if recvData:
                    print("接收到来自[%s]的消息:%s"%(client_addr, recvData))
                else:
                    print("[%s]客户端已经关闭"%client_addr)
                    client_socket.close()
                    socket_list.remove(client_socket)
            except Exception as result:
                pass
        time.sleep(1)

if __name__ == '__main__':
    main()
