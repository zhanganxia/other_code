#注意点
#1.线程之间执行顺序是无序的
#2.主线程会等待所有的子线程任务执行完成以后程序再退出
import time
import threading

#任务1
def work1():
    print("子线程:",threading.current_thread())
    while True:
        print("工作中")