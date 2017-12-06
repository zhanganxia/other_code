#encoding=utf-8
import threading
import time

num = 0

def write_num():
    global num

    # #上锁
    lock.acquire()
    for i in range(1000000):
        #在关键位置添加互斥锁，不同进程之间可以交替进行
        #lock.acquire()
        num += 1 
        #lock.release()      
    print(num)
    #释放锁
    lock.release()
def read_num():
    global num
    #上锁
    lock.acquire()
    for i in range(1000000):
        # lock.acquire()
        num += 1
        #lock.release()
    print("线程2的运行结果:%d"%num)
    #释放锁
    lock.release()
if __name__ == '__main__':

    write_thread = threading.Thread(target=write_num)
    read_thread = threading.Thread(target=read_num)

    #创建锁
    lock = threading.Lock()

    write_thread.start()
    read_thread.start()
    

