import threading
import time

#定义全局列表
mylist = []

#写入数据任务
def write_data():
    for i in range(5):
        mylist.append(i)
        time.sleep(0.1)

#读取数据的任务
def read_data():
    print(mylist)

if __name__ == '__main__':
    #创建两个子线程
    write_thread = threading.Thread(target=write_data)

    read_thread = threading.Thread(target=read_data)

    #开启线程执行任务
    write_thread.start()
    #延时调用读取数据任务的操作，主线程休眠1秒钟
    #time.sleep(1)
    #主线程等待写入线程执行完成以后再执行后面的代码
    write_thread.join()
    print("主线程休眠完了，可以执行读取数据的任务了")

    read_thread.start()
    #提示：线程之间可以共享全局变量


