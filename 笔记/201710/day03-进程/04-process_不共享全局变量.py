import multiprocessing
import time

#定义全局变量
mylist = []

#写入数据的任务
def write_data():
    for i in range(8):
        mylist.append(i)
        time.sleep(0.1)

    print("写入进程的mylist的数据为：",mylist)

#读取数据的任务
def read_data():
    print("读取到的数据为%s"%mylist)

if __name__ == '__main__':
    #创建写入和读取的进程
    write_process = multiprocessing.Process(target=write_data)
    read_process = multiprocessing.Process(target=read_data)

    write_process.start()

    #等待写入进程执行完成以后代码再继续往下执行
    write_process.join()
    #总结：进程之间不共享全局变量
    read_process.start()


