import multiprocessing
import time
import os

def work1():
    #获取子进程的进程id
    print('子进程运行中，pid=%d...'%os.getpid())
    print("当前线程是：%s"%multiprocessing.current_process())
    #获取子进程的父进程的id -->使用os.getppid()
    print('子进程父进程，pid=%d...'%os.getppid())
    for i in range(5):
        i+=1
        print("work1工作中......")
        time.sleep(1)

if __name__ == '__main__':
    #os.getpid:获取当前进程的进程号
    print("父进程pid：%d"% os.getpid())
    work1_process = multiprocessing.Process(target=work1)
    #设置work1_process为守护主进程，主进程退出了，子进程直接销毁，不再执行代码
    #work1_process.daemon = True    

    work1_process.start()
    print(multiprocessing.current_process())
    for i in range(5):
        i+=1
        print("主process执行")
        time.sleep(1)
    work1_process.terminate()
    exit()
    
