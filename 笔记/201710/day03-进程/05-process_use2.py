import multiprocessing
import time

#向消息队列写入数据
def write_data(queue):
    for i in range(10):
        #判断消息队列是否满了：
        if queue.full():
            break
        #向消息队列写入消息
        queue.put(i)
        time.sleep(0.1)

def read_data(queue):
    while True:
        if queue.full():
            break
        print(queue.get())

if __name__ == '__main__':
    #创建消息队列
    queue = multiprocessing.Queue(6)
    write_process = multiprocessing.Process(target=write_data)
    read_process = multiprocessing.Process(target=read_data)

    write_process.start()
    write_process.join()
    read_process.start()   

    #进程之间可以使用消息队列完成数据的通信 