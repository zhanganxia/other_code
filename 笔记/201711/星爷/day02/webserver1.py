#Tcp/http:服务器优化
import socket
import multiprocessing

#传输格式
#1.http版本号:  HTTP/1.1 200 OK
#2.Server: My server
#3.body: hello world

#
def handle_msg(web_client_socket):
    request_data = web_client_socket.recv(1024)
    print("request Date:",request_data)

    #格式化消息
    request_start_line = "HTTP/1.1 200 OK\r\n"
    request_head_line = "My server\r\n"
    request_body = "hello world"

    #拼接消息
    reponse_data = request_start_line +request_head_line+"\r\b"+request_body
    print("要发送的消息:",request_data)

    web_client_socket.send(bytes(reponse_data,"utf-8"))

    web_client_socket.close()

    return request_data

if __name__ == '__main__':
    web_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #设置程序退出,立即释放端口
    web_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)

    web_server_socket.bind(('',8080))
    #设置监听
    web_server_socket.listen(128)

    while True:
        web_client_socket,client_addr = web_server_socket.accept()
        print(web_client_socket,client_addr)

        #创建子进程,处理发送文件信息
        send_msg_process = multiprocessing.Process(target = handle_msg,args=(web_client_socket,))

        send_msg_process.start()
        web_client_socket.close()
        #设置守护主进程
        send_msg_process.join()

    web_server_socket.close()


    




